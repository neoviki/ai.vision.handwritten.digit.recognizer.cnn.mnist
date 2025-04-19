'''

PyTorch Tensor Wrapper [ Quick Hack Functions ]

Author:

V Natarajan (a) Viki
www.viki.design

'''


from __future__ import print_function
import torch
import numpy as np
import cv2

import lib_ui as UI
from lib_logger import *
from lib_mnist_wrapper import *


def TensorDetails(tensor):
    print("TENSOR > TOTAL NO ELEMENTS        : "+str(tensor.numel()))
    print("TENSOR > SHAPE                    : "+str(tensor.shape))
    print("TENSOR > DIMENSIONS | RANK | AXES : "+str(len(tensor.shape)))

def ReadImage(file_name):
    image = cv2.imread(file_name, 0)
    return image

def ReadImageAsTensor(file_name):
    image = ReadImage(file_name)
    tensor_image = torch.tensor(image, dtype=torch.float)
    TensorDetails(tensor_image)
    #convert array[28][28] to array[1][1][28][28]
    tensor_image = tensor_image.reshape(1, 1, 28, 28)
    tensor_image.type(torch.FloatTensor)
    TensorDetails(tensor_image)
    return tensor_image

