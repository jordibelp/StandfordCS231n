from .layers import *


def affine_relu_forward(x, w, b):
    """
    Convenience layer that perorms an affine (FCL) transform followed by a ReLU

    Inputs:
    - x: Input to the affine layer
    - w, b: Weights for the affine layer

    Returns a tuple of:
    - out: Output from the ReLU
    - cache: Object to give to the backward pass
    """
    a, fc_cache = affine_forward(x, w, b) #a is the output of the linear classifier
    out, relu_cache = relu_forward(a)
    complete_cache = (fc_cache, relu_cache)
    return out, complete_cache


def affine_relu_backward(dout, cache):
    """
    Backward pass for the affine-relu convenience layer
    """
    fc_cache, relu_cache = cache
    #backprop from the prev layer <--- dout
    da = relu_backward(dout, relu_cache)
    dx, dw, db = affine_backward(da, fc_cache)
    return dx, dw, db
