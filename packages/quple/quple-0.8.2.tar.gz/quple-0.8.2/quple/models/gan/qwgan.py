from quple.models import QGAN

import tensorflow as tf

class QWGAN(QGAN):
    """Quantum Generative Adversarial Network (QGAN)
    """    
    def __init__(self, *args, n_critic:int=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_critic = n_critic

    @tf.function
    def D_loss(self, real_output, fake_output):
        """Compute discriminator loss."""
        return tf.reduce_mean(fake_output) - tf.reduce_mean(real_output)
    
    @tf.function
    def G_loss(self, fake_output):
        """Compute generator loss."""
        return -tf.reduce_mean(fake_output)
    
    @tf.function 
    def G_step(self):
        """Perform one training step for generator"""
        # using Gaussian noise with mean 0 and width 1 as generator input
        noise = tf.random.normal((self.batch_size, self.latent_dim))
        with tf.GradientTape() as t:
            x_fake = self.G(noise, training=True)
            fake_output = self.D(x_fake, training=True)
            loss = self.G_loss(fake_output)
        grad = t.gradient(loss, self.G.trainable_variables)
        self.G_optimizer.apply_gradients(zip(grad, self.G.trainable_variables))
        return loss
    
    @tf.function
    def D_step(self, x_real):
        """Perform one training step for discriminator"""
        # using Gaussian noise with mean 0 and width 1 as generator input
        batchsize = tf.gather(tf.shape(x_real), 0)
        noise = tf.random.normal((batchsize, self.latent_dim))
        with tf.GradientTape() as t:
            x_fake_ = self.G(noise, training=True)
            x_fake = tf.reshape(x_fake_, tf.shape(x_real))
            real_output = self.D(x_real, training=True)
            fake_output = self.D(x_fake, training=True)
            # compute Wasserstein loss: (x_fake - x_real) + gp_weight*gradient_term
            cost = self.D_loss(real_output, fake_output)
            # since tfq does not supoprt 2nd order derivative we can't evaluate
            # cost with gradient penalty for the moment
            #gp = self.gradient_penalty(partial(self.D, training=True), x_real, x_fake)
            #cost = self.weight_gp * gp
        grad = t.gradient(cost, self.D.trainable_variables)
        self.D_optimizer.apply_gradients(zip(grad, self.D.trainable_variables))
        return cost  
    
    @tf.function
    def train_step(self, batch, real_noise=0.0):
        """Training step for one epoch"""
        for _ in range(self.n_critic):
            d_loss = self.D_step(batch)
        g_loss = self.G_step()
        return g_loss, d_loss

    @tf.function
    def gradient_penalty(self, f, x_real, x_fake):
        alpha = tf.random.uniform([self.batch_size, 1], 0., 1.)
        diff = x_fake - x_real
        inter = x_real + (alpha * diff)
        with tf.GradientTape() as t:
            t.watch(inter)
            pred = f(inter)
        grad = t.gradient(pred, [inter])[0]
        slopes = tf.sqrt(tf.reduce_sum(tf.square(grad), axis=1))
        gp = tf.reduce_mean((slopes - 1.)**2)
        return gp    