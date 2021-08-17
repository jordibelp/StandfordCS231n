from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange


def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    num_train = X.shape[0]
    dim = X.shape[1]
    
    for i in range(num_train):
        
        #scores_i = np.dot(W.T, X[i,:]) #(10,3073) @ (3073,) == (10,)
        scores_i = X[i,:] @ W #(1, 3073) @ (3073, 10) == (10,)
        #expos == unormalized_probs
        
        logC_term = -np.max(scores_i)
        
        scores_i += logC_term
        expos = np.exp(scores_i) 
        
        sum_expos = np.sum(expos)
        probs_i = expos/sum_expos
        losses = -np.log(probs_i)
        
        c_label = y[i]
        
        loss += losses[c_label]
        
        
        for j in range(W.shape[1]):
            
            if j == c_label:
                #term  = probs_i[c_label]**2 * (1- probs_i[c_label]) * X[i,:]
                term = - X[i,:]
            else:
                #term = - probs_i[j] * probs_i[c_label] * X[i,:]
                term = X[i,:] * probs_i[j]
                
            dW[:,j] += term    
        
    #inculding the regularization term
    loss = loss/num_train + reg * np.sum(W**2)
    dW = dW/num_train + 2 * reg * W
    
    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    num_train = X.shape[0]
    dim_size = W.shape[1]
    scores = X @ W
    #correct_class_scores = scores[np.arange(num_train), y]
    
    scores = scores - (np.max(scores, axis = 1)).reshape((num_train, 1))
    expos = np.exp(scores)
    probs = expos / np.sum(expos, axis = 1, keepdims = True)
    
    loss = np.sum(-np.log(probs[np.arange(num_train), y])) / num_train
    loss = loss + reg * np.sum(W**2)
    
    probs[np.arange(num_train), y] = - 1
    dW = X.T @ probs #(D, N) @ (N,C) == (D,C)
    
    dW = dW/num_train + 2 * reg * W 
    
    
    
    
    pass

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW