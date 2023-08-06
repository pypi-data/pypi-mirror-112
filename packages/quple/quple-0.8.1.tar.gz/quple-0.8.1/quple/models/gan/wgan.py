from quple.models import QGAN

class QWGAN(QGAN):
    """Quantum Generative Adversarial Network (QGAN)
    """    
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)

    @tf.function
    def D_loss(self, real_output, fake_output):
        """Compute discriminator loss."""
        real_loss = self.cross_entropy(tf.ones_like(real_output), real_output)
        fake_loss = self.cross_entropy(tf.zeros_like(fake_output), fake_output)
        total_loss = real_loss + fake_loss
        return total_loss
    
    @tf.function
    def G_loss(self, fake_output):
        """Compute generator loss."""
        return self.cross_entropy(tf.ones_like(fake_output), fake_output)