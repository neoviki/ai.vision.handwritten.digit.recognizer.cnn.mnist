'''
PyTorch Wrapper to work with MNIST Handwritten Digit Database

Author:

V Natarajan (a) Viki
www.viki.design

'''


import torchvision
from torchvision import transforms
import torch
from torchvision import datasets
import os
import errno
from lib_logger import *

log = logger()

import os
from torchvision import datasets, transforms

def Download_MNIST_TrainingData(path):
    print(log._st + "CHECKING MNIST TRAINING DATA")
    processed_file = os.path.join(path, 'MNIST', 'processed', 'training.pt')
    if os.path.exists(processed_file):
        print(log._ed + "MNIST TRAINING DATA ALREADY EXISTS")
        download = False
    else:
        print(log._st + "TRAINING DATA NOT FOUND, DOWNLOADING...")
        download = True

    tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    data_object = datasets.MNIST(path, train=True, download=download, transform=tf)
    print(log._ed + "MNIST TRAINING DATA READY")
    return data_object


def Download_MNIST_TestData(path):
    print(log._st + "CHECKING MNIST TEST DATA")
    processed_file = os.path.join(path, 'MNIST', 'processed', 'test.pt')
    if os.path.exists(processed_file):
        print(log._ed + "MNIST TEST DATA ALREADY EXISTS")
        download = False
    else:
        print(log._st + "TEST DATA NOT FOUND, DOWNLOADING...")
        download = True

    n_mean = 0.5
    n_std  = 0.5
    tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize((n_mean,), (n_std,))])
    data_object = datasets.MNIST(path, train=False, download=download, transform=tf)
    print(log._ed + "MNIST TEST DATA READY")
    return data_object

def Load_MNIST_Data(data_object, batch_size):
    print(log._st+ "LOADING MNIST DATA")
    tud = torch.utils.data
    data = tud.DataLoader(data_object, batch_size=batch_size, shuffle=True)
    print(log._ed+ "LOADING MNIST DATA")
    return data


def save_image(numpy_array, file_name):
    image_name = file_name + str(".png")
    tensor_array = torch.from_numpy(numpy_array)
    torchvision.utils.save_image(tensor_array, image_name)

def StoreDataAsImage(mnist_data, dfolder):

    try:
        os.mkdir(dfolder)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

    file_base = "number"

    '''
    MNIST training data has 938 records. Each record in MNIST has the following
        1. images of shape [64, 1, 28, 28]  -> 64 handwritten digits
        2. labels for images of shape [64]  -> 64 label for the 64 handwritten digit images
    '''
    '''Full Download : 938'''
    #no_records_to_store = len(mnist_data)

    '''Only 64 Images Download'''
    no_records_to_store = 1

    #Iterate Over MNIST DATA
    for i, data in enumerate(mnist_data, 0):

        if(i >= no_records_to_store):
            break

        images, labels = data

        for j in range(len(images)):
            file_name = dfolder+str("/")+file_base+"_"+str(labels[j].item())+"_"+str(i)+"_"+str(j)

            '''
            Pixel Values will be in range between -1 and 1
            '''
            normalized_image = images[j][0]
            n_mean = 0.5
            n_std = 0.5
            '''
            Pixel Values will be in range between 0 and 1
            '''
            denormalized_image = (normalized_image * n_std) + n_mean
            image_numpy_array = denormalized_image.numpy()
            save_image(image_numpy_array, file_name)

'''
mnist_path = 'data/1.training.and.test.data/MNIST'
image_path = 'data/3.ai.model.verification.images'
training_batch_size = 64
test_batch_size = 1000

training_object = Download_MNIST_TrainingData(mnist_path)
test_object     = Download_MNIST_TestData(mnist_path)

training_data   = Load_MNIST_Data( training_object, training_batch_size   )
test_data       = Load_MNIST_Data( test_object,     test_batch_size       )

StoreDataAsImage(training_data, image_path)
'''
