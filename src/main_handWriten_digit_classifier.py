'''
Handwritten Digit Classifier

Author  : Viki (a) V Natarajan
Contact : www.viki.design
'''
import sys
import lib_ui as UI
from lib_mnist_wrapper import *
from cnn import *
from lib_tensor_wrapper import *
import os
from lib_logger import *
log             = logger()

net             = None

mnist_path      = 'data/1.training.and.test.data'
image_path      = 'data/3.ai.model.verification.images'
model_path              = 'data/2.ai.model'

model_file              = model_path + '/' + 'torch.pt'

training_batch_size = 64
#training_batch_size = 128
test_batch_size     = 1000
learning_rate       = 0.001
momentum            = 0.9


def ui_callback(file_name):
    global net
    tensor = ReadImageAsTensor(file_name)
    prediction   = ClassifyImage(net, tensor)
    return prediction

def download():
    global training_data, test_data, mnist_training_data_object, mnist_test_data_object
    global training_data, test_data
    mnist_training_data_object  = Download_MNIST_TrainingData(mnist_path)
    mnist_test_data_object      = Download_MNIST_TestData(mnist_path)

def load():
    global training_data, test_data, mnist_training_data_object, mnist_test_data_object
    training_data   = Load_MNIST_Data( mnist_training_data_object, training_batch_size   )
    test_data       = Load_MNIST_Data( mnist_test_data_object,     test_batch_size       )


def init_cnn():
    global net, training_data, test_data, mnist_training_data_object, mnist_test_data_object
    ''' Initialize CNN '''
    if os.path.exists(model_file):
        net = LoadModel(model_file)
        print(log._if+ "LoadModel CNN Model")
    else:
        print(log._er+ "LoadModel CNN Model")
        net = CNN()
        ''' Common loss function for classification
        '''
        loss_function = nn.CrossEntropyLoss()
        parameters = net.parameters()
        betas = (0.9, 0.999)

        ''' Create an Optimizer '''
        #optimizer  = Optimizer_SGD(parameters, learning_rate, momentum)
        ''' ADAM Optimizer Learning is fast '''
        optimizer = Optimizer_ADAM(parameters, learning_rate, betas)

        train_cnn(net, training_data, training_batch_size, optimizer, loss_function)
        SaveModel(net, model_file)



def create_essential_dirs():
    os.makedirs(model_path, exist_ok=True)

def main():
    create_essential_dirs()
    download()
    load()
    init_cnn()
    UI.render(ui_callback, image_path)

main()
