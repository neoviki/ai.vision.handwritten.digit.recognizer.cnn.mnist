'''
Handwritten Digit Classifier

Author  : Viki (a) V Natarajan
Contact : www.viki.design
'''
import sys
#sys.path.append('../packages')

import lib_ui as UI
from lib_logger import *
from lib_mnist_wrapper import *
from lib_cnn import *
from tensor_wrapper import *

log             = logger()
net             = None

mnist_path      = 'data'
image_path      = 'data/3.ai.model.verification.images'
model_file      = 'data/2.ai.model/torch.pt'

training_batch_size = 64
#training_batch_size = 128
test_batch_size     = 1000
learning_rate       = 0.001
momentum            = 0.9


def ui_callback(file_name):
    global net
    tensor       = ReadImageAsTensor(file_name)
    prediction   = ClassifyImage(net, tensor)
    return prediction


training_object = Download_MNIST_TrainingData(mnist_path)
test_object     = Download_MNIST_TestData(mnist_path)

training_data   = Load_MNIST_Data( training_object, training_batch_size   )
test_data       = Load_MNIST_Data( test_object,     test_batch_size       )


''' Initialize CNN '''
try:
    net = LoadModel(model_file)
except:
    pass

if not net:
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
else:
    print(log._if+ "LoadModel CNN Model")


UI.render(ui_callback, image_path)

'''
test_cnn(net, test_data)
evaluate_cnn(net, test_data)
visualize_cnn_hidden_layer_activation(net, test_data)
'''

