# based on the work by Dongwei Chen+ 2020
# "Deep Residual Learning for Nonlinear Regression"
# https://www.mdpi.com/1099-4300/22/2/193
#  https://github.com/DowellChan/ResNetRegression

# https://github.com/tiantiy/ResNetRegression/blob/master/ResNetOptimalModel.py

from tensorflow.keras import layers
from tensorflow.keras import models


def identity_block(input_tensor, units, batch_norm, momentum=0.99):
    """The identity block is the block that has no conv layer at shortcut.
    # Arguments
            input_tensor: input tensor
            units:output shape
            batch_norm: bool - use batch normalization or not
    # Returns
            Output tensor for the block.
    """
    x = layers.Dense(units)(input_tensor)
    if batch_norm:
        x = layers.BatchNormalization(momentum=momentum)(x)
    x = layers.Activation("relu")(x)

    x = layers.Dense(units)(x)
    if batch_norm:
        x = layers.BatchNormalization(momentum=momentum)(x)
    x = layers.Activation("relu")(x)

    x = layers.Dense(units)(x)
    if batch_norm:
        x = layers.BatchNormalization(momentum=momentum)(x)

    x = layers.add([x, input_tensor])
    x = layers.Activation("relu")(x)

    return x


def dens_block(input_tensor, units, batch_norm, momentum=0.99):
    """A block that has a dense layer at shortcut.
    # Arguments
            input_tensor: input tensor
            unit: output tensor shape
            batch_norm: bool - use batch normalization or not
    # Returns
            Output tensor for the block.
    """
    x = layers.Dense(units)(input_tensor)
    if batch_norm:
        x = layers.BatchNormalization(momentum=momentum)(x)
    x = layers.Activation("relu")(x)

    x = layers.Dense(units)(x)
    if batch_norm:
        x = layers.BatchNormalization(momentum=momentum)(x)
    x = layers.Activation("relu")(x)

    x = layers.Dense(units)(x)
    if batch_norm:
        x = layers.BatchNormalization(momentum=momentum)(x)

    shortcut = layers.Dense(units)(input_tensor)
    if batch_norm:
        shortcut = layers.BatchNormalization(momentum=momentum)(shortcut)

    x = layers.add([x, shortcut])
    x = layers.Activation("relu")(x)
    return x


def ResNet(
    input_shape, output_shape, width=64, num_blocks=3, batch_norm=True, momentum=0.99
):
    """builds a ResNet regression model
    # Arguments
            input_shape: number of inputs
            output_shape: number of outputs
            width [64]:
            num_blocks [3]: total number of blocks. A block consists of
                            a dense block followed by two identity blocks.
            batch_norm [True]: bool, use batch normalization layers or not
    # Returns
            A Keras model instance.
    """
    assert num_blocks >= 1, f"num_blocks={num_blocks} not allowed. must be >= 1"

    Res_input = layers.Input(shape=(input_shape,))

    x = dens_block(Res_input, width, batch_norm=batch_norm, momentum=momentum)
    x = identity_block(x, width, batch_norm=batch_norm, momentum=momentum)
    x = identity_block(x, width, batch_norm=batch_norm, momentum=momentum)

    if num_blocks > 1:
        for i in range(1, num_blocks):
            x = dens_block(x, width, batch_norm=batch_norm, momentum=momentum)
            x = identity_block(x, width, batch_norm=batch_norm, momentum=momentum)
            x = identity_block(x, width, batch_norm=batch_norm, momentum=momentum)

    if batch_norm:
        x = layers.BatchNormalization(momentum=momentum)(x)
    x = layers.Dense(output_shape, activation="linear")(x)
    model = models.Model(inputs=Res_input, outputs=x)

    return model
