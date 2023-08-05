import numpy as np
import tensorflow as tf
from tensorflow.keras import layers as kl
from tensorflow.keras.initializers import VarianceScaling
from koogu.data.tf_transformations import spatial_split


def build_model(inputs, arch_params, **kwargs):

    patch_size, patch_overlap = 81, 18
    rejoin_block_num = 4

    data_format = 'channels_last' if 'data_format' not in kwargs else kwargs['data_format']

    f_axis, t_axis, channel_axis, old_format = (1, 2, 3, 'NHWC') if data_format == 'channels_last' else (2, 3, 1, 'NCHW')

    layers_per_block = arch_params['layers_per_block']
    pool_sizes = arch_params['pool_sizes']
    pool_strides = arch_params['pool_strides']

    # Split along the frequency axis and concatenate along the batch axis
    outputs = spatial_split(inputs, f_axis, patch_size, patch_overlap, old_format)
    freq_split_num_pieces = len(outputs)
    outputs = tf.concat(outputs, axis=0)
    #print('Num freq splits = {:d}'.format(freq_split_num_pieces))

    # Build DenseNET
    arch_params['layers_per_block'] = layers_per_block[:rejoin_block_num]
    arch_params['pool_sizes'] = pool_sizes[:rejoin_block_num]
    arch_params['pool_strides'] = pool_strides[:rejoin_block_num]
    arch_params['semi_dense'] = True
    outputs = densenet_base(outputs, arch_params, **kwargs)

    # If splitting of features (for "FCN") was done above, "undo" it.
    if freq_split_num_pieces > 0:
        # Split along the batch axis and concatenate along the leaf nodes axis
        outputs = tf.concat(tf.split(outputs, freq_split_num_pieces, axis=0),
                            axis=f_axis)

    # Do another DenseNET after reverting the frequency axis
    arch_params['layers_per_block'] = layers_per_block[rejoin_block_num:]
    arch_params['pool_sizes'] = pool_sizes[rejoin_block_num:]
    arch_params['pool_strides'] = pool_strides[rejoin_block_num:]
    arch_params['semi_dense'] = False
    outputs = densenet_base(outputs, arch_params, start_block=rejoin_block_num, **kwargs)

    # Final batch_norm & activation
    outputs = kl.BatchNormalization(axis=channel_axis, fused=True, scale=False, epsilon=1e-8)(outputs)
    outputs = kl.Activation('relu', name='ReLu')(outputs)

    # Pooling or flattening
    if 'flatten_leaf_nodes' in arch_params and arch_params['flatten_leaf_nodes']:  # if flattening is enabled
        outputs = kl.Flatten(data_format=data_format)(outputs)
    else:
        # This is the default - take global mean
        outputs = kl.GlobalAveragePooling2D(data_format=data_format)(outputs)

    return outputs


def densenet_base(inputs, arch_params, start_block=0, **kwargs):

    data_format = 'channels_last' if 'data_format' not in kwargs else kwargs['data_format']
    dropout_rate = 0.0 if 'dropout_rate' not in kwargs else kwargs.pop('dropout_rate')

    channel_axis = 3 if data_format == 'channels_last' else 1

    version = arch_params['version']
    # Parameters configurable as per the DenseNET paper
    growth_rate = arch_params['growth_rate']
    with_bottleneck = arch_params['with_bottleneck']
    compression = arch_params['compression']
    # Parameters that are my additions
    semi_dense = arch_params.get('semi_dense', False)
    implicit_pooling = arch_params.get('implicit_pooling', False)

    pooling = kl.MaxPooling2D if 'pooling_type' in arch_params and arch_params['pooling_type'] == 'max' \
        else kl.AveragePooling2D

    def composite_fn(cf_inputs, num_filters, kernel_size, strides, padding, cf_idx, n_pre=''):
        name_prefix = n_pre + 'CF{}_'.format(cf_idx)

        cf_outputs = kl.BatchNormalization(axis=channel_axis, fused=True, scale=False,
                                           name=name_prefix + 'BatchNorm')(cf_inputs)
        cf_outputs = kl.Activation('relu', name=name_prefix + 'ReLu')(cf_outputs)
        cf_outputs = kl.Conv2D(filters=num_filters, kernel_size=kernel_size, strides=strides,
                               padding=padding, use_bias=False, data_format=data_format,
                               kernel_initializer=VarianceScaling(),
                               name=name_prefix + 'Conv2D')(cf_outputs)

        if dropout_rate > 0.0:
            cf_outputs = kl.Dropout(dropout_rate, name=name_prefix + 'Dropout')(cf_outputs)

        return cf_outputs

    def dense_block(db_inputs, num_layers_in_block, b_idx):

        name_prefix = 'B{:d}_'.format(b_idx)

        db_outputs = [db_inputs]

        for layer in range(num_layers_in_block):
            if not semi_dense and len(db_outputs) > 1:
                db_outputs = [kl.Concatenate(axis=channel_axis,
                                             name=name_prefix + 'Concat{:d}'.format(layer + 1))(db_outputs)]

            if with_bottleneck:
                layer_outputs = composite_fn(db_outputs[-1], growth_rate * 4, [1, 1], [1, 1], 'same',
                                             '-BtlNk{:d}'.format(layer + 1), name_prefix)
            else:
                layer_outputs = db_outputs[-1]

            layer_outputs = composite_fn(layer_outputs, growth_rate, [3, 3], [1, 1], 'same',
                                         (layer + 1), name_prefix)

            db_outputs.append(layer_outputs)

        return kl.Concatenate(axis=channel_axis, name=name_prefix + 'Concat')(db_outputs)

    outputs = inputs

    # Initial convolution, if enabled.
    if arch_params['first_conv_filters'] is not None or (with_bottleneck and compression < 1.0):
        outputs = kl.Conv2D(filters=((2 * growth_rate) if (with_bottleneck and compression < 1.0)
                                     else arch_params['first_conv_filters']),
                            kernel_size=arch_params['first_conv_size'],
                            strides=arch_params['first_conv_strides'],
                            padding='same', use_bias=False, data_format=data_format,
                            kernel_initializer=VarianceScaling(),
                            name='PreConv2D')(outputs)

    # Initial pooling
    if arch_params['first_pool_size'] is not None and arch_params['first_pool_strides'] is not None:
        outputs = kl.MaxPooling2D(pool_size=arch_params['first_pool_size'],
                                  strides=arch_params['first_pool_strides'],
                                  padding='same', data_format=data_format,
                                  name='initial_pooling')(outputs)

    # Add N dense blocks, succeeded by transition layers as applicable
    for block_idx, num_layers in enumerate(arch_params['layers_per_block']):
        # Dense block
        outputs = dense_block(outputs, num_layers, block_idx + 1 + start_block)

        # Transition layer.
        # If implicit_pooling is set, add transition layers for all dense blocks. Otherwise,
        # add transition layers for all but the last dense block.
        if block_idx < len(arch_params['layers_per_block']) - 1 or implicit_pooling:
            # Transition layer
            if compression < 1.0:  # if compression is enabled
                num_features = int(outputs.get_shape().as_list()[channel_axis] * compression)
            else:
                num_features = outputs.get_shape().as_list()[channel_axis]

            # Ensure that pixels at boundaries are properly accounted for when stride > 1.
            outputs = pad_for_valid_conv(outputs,
                                         arch_params['pool_sizes'][block_idx],
                                         arch_params['pool_strides'][block_idx],
                                         data_format)

            if implicit_pooling:    # Achieve pooling by strided convolutions
                outputs = composite_fn(outputs, num_features,
                                       arch_params['pool_sizes'][block_idx],
                                       arch_params['pool_strides'][block_idx],
                                       'valid', '', n_pre='T{:d}_'.format(block_idx + 1 + start_block))
            else:
                outputs = composite_fn(outputs, num_features, [1, 1], [1, 1], 'valid', '',
                                       n_pre='T{:d}_'.format(block_idx + 1 + start_block))

                outputs = pooling(pool_size=arch_params['pool_sizes'][block_idx],
                                  strides=arch_params['pool_strides'][block_idx],
                                  padding='valid', data_format=data_format,
                                  name='T{:d}_Pool'.format(block_idx + 1 + start_block))(outputs)

    return outputs


def pad_for_valid_conv(inputs, kernel_shape, strides, data_format):
    # Ensure that pixels at boundaries are properly accounted for when stride > 1.

    f_axis, t_axis = (1, 2) if data_format == 'channels_last' else (2, 3)

    feature_dims = inputs.get_shape().as_list()
    outputs = inputs

    spatial_dims = np.asarray([feature_dims[f_axis], feature_dims[t_axis]])
    remainders = spatial_dims - (
            (np.floor((spatial_dims - kernel_shape) /
             strides) * strides) +
            kernel_shape)
    if np.any(remainders):
        additional = np.where(remainders, kernel_shape - remainders, [0, 0]).astype(np.int)
        pad_amt = np.asarray([[0, 0], [0, 0], [0, 0], [0, 0]])
        pad_amt[f_axis, 1] = additional[0]
        pad_amt[t_axis, 1] = additional[1]
        outputs = tf.pad(outputs, pad_amt, mode='CONSTANT', constant_values=0)

    return outputs