import numpy as np

import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.utils import conv_utils
from tensorflow.python.framework import tensor_shape
from tensorflow.python.keras import constraints, initializers, regularizers

from quple.interface.tfq.layers import PQC
from quple.interface.tfq.tf_utils import get_output_shape

class QConv2D(PQC):
    def __init__(self, kernel_circuit,
                 data_circuit,
                 operators,
                 kernel_size,
                 strides=1,
                 padding='same',
                 trainable=True,
                 kernel_initializer=tf.keras.initializers.RandomUniform(0, 2 * np.pi),
                 kernel_regularizer=None,
                 kernel_constraint=None,               
                 name=None, **kwargs):
        self.kernel_initializer = initializers.get(kernel_initializer)
        self.kernel_regularizer = regularizers.get(kernel_regularizer)
        self.kernel_constraint = constraints.get(kernel_constraint)
        super(QConv2D, self).__init__(kernel_circuit, data_circuit, operators,
                                      trainable=trainable, name=name, **kwargs)
        self.rank = 2
        self.kernel_size = conv_utils.normalize_tuple(kernel_size, self.rank, 'kernel_size')
        self.strides = conv_utils.normalize_tuple(strides, self.rank, 'strides')
        self.padding = conv_utils.normalize_padding(padding)
        self._validate_init()
        self._input_resolver = self._get_input_resolver()
        
    def _validate_init(self):
        if not all(self.kernel_size):
            raise ValueError('The argument `kernel_size` cannot contain 0(s). '
                           'Received: %s' % (self.kernel_size,))

        if not all(self.strides):
            raise ValueError('The argument `strides` cannot contains 0(s). '
                           'Received: %s' % (self.strides,))
        kernel_size = self.kernel_size[0]*self.kernel_size[1]
        if self._n_qubit != kernel_size:
            raise ValueError(f"The kernel size (={kernel_size}) must match the number of "
                             f"data qubits (={self._n_qubit})")
            
    def build(self, input_shape):
        """Keras build function."""
        output_shape = get_output_shape(input_shape[1:], self.kernel_size, self.strides, self.padding)
        self.output_height = output_shape[0]
        self.output_width = output_shape[1]
        super().build(input_shape)
            
    def init_weights(self):
        # Weight creation is not placed in a Build function because the number
        # of weights is independent of the input shape.
        self.kernel = self.add_weight('kernel',
                                      shape=self._symbols.shape,
                                      initializer=self.kernel_initializer,
                                      regularizer=self.kernel_regularizer,
                                      constraint=self.kernel_constraint,
                                      dtype=tf.float32,
                                      trainable=True)
        
    def _get_input_resolver(self):
        kernel_size = (1, 1) + self.kernel_size + (1,)
        strides = (1, 1) + self.strides + (1,)
        padding = self.padding.upper()
        batchsize = lambda x: tf.gather(tf.shape(x), 0)
        input_height = lambda x: tf.gather(tf.shape(x), 1)
        input_width = lambda x: tf.gather(tf.shape(x), 2)
        reshaped_input = lambda x: tf.reshape(x, shape=(batchsize(x), 1, input_height(x), input_width(x), 1))
        input_patches = lambda x: tf.extract_volume_patches(reshaped_input(x),
            ksizes=kernel_size, strides=strides, padding=padding)
        resolved_input = lambda x: self._data_circuit_resolver(input_patches(x))
        return resolved_input
        
    def call(self, inputs):
        """Keras call function."""
        batchsize = tf.gather(tf.shape(inputs), 0)
        resolved_inputs_ = self._input_resolver(inputs)       
        circuit_size = tf.reduce_prod(tf.strided_slice(tf.shape(resolved_inputs_), begin=[0], end=[-1]))
        output_height = tf.gather(tf.shape(resolved_inputs_), 2)
        output_width = tf.gather(tf.shape(resolved_inputs_), 3)
        resolved_inputs = tf.reshape(resolved_inputs_, (circuit_size, tf.shape(resolved_inputs_)[-1]))     
        tiled_up_parameters_ = tf.tile([self.kernel], [circuit_size, 1])
        tiled_up_parameters = tf.concat([resolved_inputs, tiled_up_parameters_], 1)        
        
        tiled_up_data_circuit = tf.tile(self._data_circuit, [circuit_size])
        tiled_up_model = tf.tile(self._model_circuit, [circuit_size])
        model_appended = self._append_layer(tiled_up_data_circuit, append=tiled_up_model)
        
        tiled_up_operators = tf.tile(self._operators, [circuit_size, 1])

        # this is disabled to make autograph compilation easier.
        # pylint: disable=no-else-return
        if self._analytic:
            result = self._executor(model_appended,
                                   symbol_names=self._all_symbols,
                                   symbol_values=tiled_up_parameters,
                                   operators=tiled_up_operators)
        else:
            tiled_up_repetitions = tf.tile(self._repetitions,
                                           [circuit_batch_dim, 1])
            result =  self._executor(model_appended,
                                    symbol_names=self._all_symbols,
                                    symbol_values=tiled_up_parameters,
                                    operators=tiled_up_operators,
                                    repetitions=tiled_up_repetitions)
        return tf.reshape(result, (batchsize, self.output_height, self.output_width))
        # pylint: enable=no-else-return