from math import ceil
import tensorflow as tf

def get_paddings(input_shape, filter_shape, strides):
    """
    Arguments:
        input_shape: (height, width)
        filter_shape: (height, width)
        strides: (height, width)
    """
    out_height = ceil(float(input_shape[0]) / float(strides[0]))
    out_width  = ceil(float(input_shape[1]) / float(strides[1]))
    if (input_shape[0] % strides[0] == 0):
        pad_along_height = max(filter_shape[0] - strides[0], 0)
    else:
        pad_along_height = max(filter_shape[0] - (input_shape[0] % strides[0]), 0)
    if (input_shape[1] % strides[1] == 0):
        pad_along_width = max(filter_shape[1] - strides[1], 0)
    else:
        pad_along_width = max(filter_shape[1] - (input_shape[1] % strides[1]), 0)
    pad_top = pad_along_height // 2
    pad_bottom = pad_along_height - pad_top
    pad_left = pad_along_width // 2
    pad_right = pad_along_width - pad_left
    return tf.constant([[pad_top, pad_bottom,], [pad_left, pad_right]])

def get_padded_shape(input_shape, filter_shape, strides, padding="same"):
    if padding.lower() == "same":
        paddings = get_paddings(input_shape, filter_shape, strides)
        return tf.TensorShape([input_shape[0]+paddings[0][0]+paddings[0][1],
                               input_shape[1]+paddings[1][0]+paddings[1][1]])
    elif padding.lower() == "valid":
        return tf.TensorShape([input_shape[0], input_shape[1]])
    else:
        raise ValueError("invalid padding: {}".format(padding))
        
def get_output_shape(input_shape, filter_shape, strides, padding="same"):
    padded_shape = get_padded_shape(input_shape, filter_shape, strides, padding)
    out_height = ceil(float(padded_shape[0] - filter_shape[0] + 1) / float(strides[0]))
    out_width  = ceil(float(padded_shape[1] - filter_shape[1] + 1) / float(strides[1]))
    return tf.TensorShape([out_height, out_width])