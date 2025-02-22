# -*- coding: utf-8 -*-
"""
Draft code for implementation of EMD with a CNN model to train ASIC Autoencoder

Takes in a pair of numbers and then outputs their loss

There are 8 .h5 files with optimized EMD, load all of them, architecture is currently 443, look into this later

"""

import numpy as np
import pandas as pd
import math

from tensorflow.keras.layers import Input, Dense, Flatten, Concatenate, BatchNormalization, Activation, Average, Conv2D
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l1_l2
        
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import tensorflow as tf
from tensorflow.keras import backend as K

emd_model = tf.keras.models.load_model("emd_model_best.h5")
emd_model.trainable = False

remap_8x8 = [4, 12, 20, 28,  5, 13, 21, 29,  6, 14, 22, 30,  7, 15, 23, 31, 
             24, 25, 26, 27, 16, 17, 18, 19,  8,  9, 10, 11,  0,  1,  2,  3, 
             59, 51, 43, 35, 58, 50, 42, 34, 57, 49, 41, 33, 56, 48, 40, 32]

arrange443 = np.array([0,16, 32,
                       1,17, 33,
                       2,18, 34,
                       3,19, 35,
                       4,20, 36,
                       5,21, 37,
                       6,22, 38,
                       7,23, 39,
                       8,24, 40,
                       9,25, 41,
                       10,26, 42,
                       11,27, 43,
                       12,28, 44,
                       13,29, 45,
                       14,30, 46,
                       15,31, 47])

def map_881_to_443(x):
    y = tf.reshape(x, (-1, 64))
    y = tf.gather(y, remap_8x8, axis=1)
    y = tf.gather(y, arrange443, axis=1)
    y = tf.reshape(y, (-1, 4, 4, 3))
    return y
        
def emd_loss(y_true, y_pred):
    
    """
    Input comes in in 8x8 looking like this:
    arrange8x8 = np.array([
        28,29,30,31,0,4,8,12,
        24,25,26,27,1,5,9,13,
        20,21,22,23,2,6,10,14,
        16,17,18,19,3,7,11,15,
        47,43,39,35,35,34,33,32,
        46,42,38,34,39,38,37,36,
        45,41,37,33,43,42,41,40,
        44,40,36,32,47,46,45,44])
    Remapping using array from telescope.py
    
    """
    y_pred_443 = map_881_to_443(y_pred)
    y_true_443 = map_881_to_443(y_true)
    
    return emd_model([y_true_443, y_pred_443])
