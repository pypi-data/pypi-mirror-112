import os
from typing import Union, Optional
from functools import partial

import numpy as np
import cirq
import tensorflow as tf
from tensorflow.keras.models import Sequential
import tensorflow_quantum as tfq
from sklearn.metrics import roc_curve, auc, roc_auc_score

import quple
from quple.interface.tfq.layers.pqc import PQC
from quple.utils.utils import plot_roc_curve

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from IPython.display import display, clear_output

class QGAN(object):
    """Quantum Generative Adversarial Network (QGAN)
    """    
    def __init__(self, generator_circuit:"cirq.Circuit", discriminator_circuit:"cirq.Circuit",
                 encoding_circuit:"cirq.Circuit",
                 epochs:int=100, batch_size:int=10,   
                 g_lr:float=1e-3, d_lr:float=1e-3,
                 g_readout=None,
                 d_readout=None,                 
                 g_differentiator:Optional[tfq.differentiators.Differentiator]=None,
                 d_differentiator:Optional[tfq.differentiators.Differentiator]=None,
                 regularizer=None,
                 repetitions=None,                 
                 random_state:Optional[int]=None,
                 checkpoint_dir="./training_checkpoints",
                 checkpoint_interval=15,
                 name:str='QGAN', *args, **kwargs):
        """ Creates a QGAN model equipped with a generator and a discriminator
            The only difference between WGAN and DCGAN is in the definition of
            the loss function and the discriminator step per generator step and
            possibly the choice of activation function
        Args:
            generator: cirq.Circuit or quple.QuantumCircuit instace
                A parameterised quantum circuit as a variational quantum generator (VQG)
            discriminator: cirq.Circuit or quple.QuantumCircuit instace
                A parameterised quantum circuit as a variational quantum discriminator (VQD)
            encoding_circuit: cirq.Circuit or quple.QuantumCircuit instace
                A parameterised quantum circuit for data encoding             
            epochs: int, default=100
                Number of epochs
            batch_size: int, default=10
                Batch size for training
            g_lr: float, default=1e-4
                Learning rate for the Adam optimizer of the generator
            d_lr: float, default=1e-4
                Learning rate for the Adam optimizer of the discriminator
            g_readout: `cirq.PauliSum` or Python `list` of `cirq.PauliSum` objects, default=None
                Measurement operators (observables) for the variational circuit layer of generator
                If None, defaults to Pauli Z on all qubits
            d_readout: `cirq.PauliSum` or Python `list` of `cirq.PauliSum` objects, default=None
                Measurement operators (observables) for the variational circuit layer of generator                     
                If None, defaults to Pauli Z on first qubit
            differentiator: Optional `tfq.differentiator` object 
                To specify how gradients of variational circuit should be calculated.
            regularizer: Optional `tf.keras.regularizer` object
                Regularizer applied to the parameters of the variational circuit.
            repetitions: int; default=None
                Number of repetitions for measurement           
            random_state: Optional int, default=None
                The random state for reproducible result.
            name: Optional str, default="QGAN"
                Name given to the classifier.                
        """
        # initialize hyperparameters first
        self.epochs = epochs
        self.batch_size = batch_size
        self.g_lr = g_lr
        self.d_lr = d_lr
        self.g_differentiator = g_differentiator
        self.d_differentiator = d_differentiator
        self.regularizer = regularizer
        self.repetitions = repetitions
        self.g_readout = g_readout
        self.d_readout = d_readout
        self.encoding_circuit = encoding_circuit
        # latent dimension is the same as number of features (= number of qubits)
        self.latent_dim = len(quple.get_circuit_qubits(encoding_circuit))
        self.random_state = random_state
        self.set_random_state(self.random_state)
        # create generator and discriminator models from parameterized quantum circuit
        self.G = self.create_generator(generator_circuit)
        self.D = self.create_discriminator(discriminator_circuit)
        # create optimizers
        self.G_optimizer = tf.keras.optimizers.Adam(learning_rate=self.g_lr)
        self.D_optimizer = tf.keras.optimizers.Adam(learning_rate=self.d_lr)
        
        self.cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        self.checkpoint_dir = checkpoint
        self.checkpoint_interval = checkpoint_interval
        self.checkpoint = tf.train.Checkpoint(generator_optimizer=self.G_optimizer,
                                              discriminator_optimizer=self.D_optimizer,
                                              generator=self.G,
                                              discriminator=self.D)
        self.name = name
        
        print('Summary of Generator')
        self.G.summary()
        
        print('Summary of Discriminator')
        self.D.summary()
        
    @staticmethod
    def set_random_state(random_state=None):
        tf.random.set_seed(random_state)
        np.random.seed(random_state)        
        
    def create_generator(self, quantum_circuit:"cirq.Circuit"):
        generator = Sequential()
        # input layer for feeding classical data
        input_layer = tf.keras.layers.Input(shape=(self.latent_dim), dtype=tf.float32)
        # variational layer 
        qubits = quple.get_circuit_qubits(quantum_circuit)
        if not self.g_readout:
            g_readout = [cirq.Z(qubit) for qubit in qubits]
        else:
            g_readout = self.g_readout
        pqc_layer = PQC(quantum_circuit,
                        self.encoding_circuit,
                        g_readout,
                        repetitions=self.repetitions,
                        differentiator=self.g_differentiator,
                        regularizer=self.regularizer)
        generator.add(input_layer)
        generator.add(pqc_layer)
        return generator
    
    def create_discriminator(self, quantum_circuit:"cirq.Circuit"):
        discriminator = Sequential()     
        # input layer for feeding classical data
        input_layer = tf.keras.layers.Input(shape=(self.latent_dim), dtype=tf.float32)
        # variational layer 
        qubits = quple.get_circuit_qubits(quantum_circuit)
        if not self.d_readout:
            # by default measure PauliZ on first qubit
            d_readout = [cirq.Z(qubits[0])]
        else:
            d_readout = self.d_readout    
        pqc_layer = PQC(quantum_circuit,
                        self.encoding_circuit,
                        d_readout,
                        repetitions=self.repetitions,
                        differentiator=self.d_differentiator,
                        regularizer=self.regularizer)
        discriminator.add(input_layer)
        # create generator model
        discriminator.add(pqc_layer)
        return discriminator
    
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
    
    @tf.function
    def to_prob(self, x):
        """Convert discriminator output to probabilities"""
        return tf.divide(tf.add(x, 1), 2)
    
    @tf.function
    def train_step(self, x_real, real_noise=0.0):
        """Training step for one epoch"""
        noise = tf.random.normal([self.batch_size, self.latent_dim])
        #x_real_w_noise = tf.add(x_real, tf.random.normal(shape=x_real.shape, 
        #                                           mean=0.0, 
        #                                           stddev=real_noise, dtype=x_real.dtype))
        with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
            x_fake = self.G(noise, training=True)
            real_output = self.D(x_real, training=True)
            #p_real = self.to_prob(real_output) 
            fake_output = self.D(x_fake, training=True)
            #p_fake = self.to_prob(fake_output) 
            gen_loss = self.G_loss(fake_output)
            disc_loss = self.D_loss(real_output, fake_output)
        grad_gen = gen_tape.gradient(gen_loss, self.G.trainable_variables)
        grad_disc = disc_tape.gradient(disc_loss, self.D.trainable_variables)
        self.G_optimizer.apply_gradients(zip(grad_gen, self.G.trainable_variables))
        self.D_optimizer.apply_gradients(zip(grad_disc, self.D.trainable_variables))  
        return gen_loss, disc_loss
    
    def generate_samples(self, batch_size):
        """Generates sample using random inputs."""
        z = tf.random.normal((batch_size, self.latent_dim))
        return self.G(z, training=False)  
    
    def predict(self, x):
        return self.D(x, training=False)
    
    @staticmethod
    def create_batches(x, batch_size, buffer_size=10000):
        batches = tf.data.Dataset.from_tensor_slices(x).shuffle(buffer_size).batch(batch_size)
        return batches
    
    def train(self, x, interactive_display=True):
        self.set_random_state(self.random_state)
        batches = self.create_batches(x, self.batch_size)
        #sample_size = x.shape[0]
        #z = tf.constant(tf.random.normal((sample_size, self.latent_dim)))
        g_metric = tf.keras.metrics.Mean()
        d_metric = tf.keras.metrics.Mean()
        fig = plt.figure(figsize=(16,9))
        g_loss_arr = []
        d_loss_arr = []
        epoch_arr = []
        checkpoint_prefix = os.path.join(self.checkpoint_dir, "ckpt")
        for epoch in range(self.epochs):
            for batch in batches:
                gen_loss, disc_loss = self.train_step(batch)
                g_metric(gen_loss)
                d_metric(disc_loss)
                
            g_loss_arr.append(g_metric.result().numpy())
            d_loss_arr.append(d_metric.result().numpy())
            epoch_arr.append(epoch)
            if interactive_display:
                self.display_loss(g_loss_arr, d_loss_arr, epoch_arr)
            g_metric.reset_states()
            d_metric.reset_states()
            
            if ((epoch + 1) % self.checkpoint_interval == 0):
                self.checkpoint.save(file_prefix=checkpoint_prefix)
        return g_loss_arr, d_loss_arr
    
    def test(self, x, y, plot=True):
        score = self.predict(x)
        fpr, tpr, thresholds = roc_curve(y, score)
        roc_auc = auc(fpr, tpr)
        if plot:
            return plot_roc_curve(fpr, tpr, 'QDCGAN')
        else:
            return roc_auc
    
    def get_weights(self):
        weights = {
            'generator': self.G.get_weights()[0],
            'discriminator': self.D.get_weights()[0]
        }
        return weights
    
    def save_weights(self, fname='weights.npz'):
        weights = self.get_weights()
        np.savez(fname, **weights)
        
    def load_weights(self, fname='weights.npz'):
        weights = dict(np.load(fname, allow_pickle=True))
        generator_weights = weights['generator']
        discrminator_weights = weights['discriminator']
        self.G.set_weights([generator_weights])
        self.D.set_weights([discrminator_weights])
    
    def display_loss(self, g_loss, d_loss, epochs):
        ax = plt.gca()
        ax.set_xlim(0, 1.1*epochs[-1])
        ax.cla()
        ax.plot(epochs, g_loss, label="Generator")
        ax.plot(epochs, d_loss, label="Discriminator")
        ax.set_xlabel('Epoch', fontsize=20)
        ax.set_ylabel('Binary Cross Entropy Loss', fontsize=20)
        ax.grid(True)
        ax.legend(fontsize=20)
        display(plt.gcf())
        clear_output(wait = True)