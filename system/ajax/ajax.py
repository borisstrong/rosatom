import os
import shutil
import numpy as np
import json
from datetime import datetime

'''
import matplotlib.pyplot as plt

from skimage.io import imread  # Чтение файла сразу в np массив, для варианта с обрезкой

import tensorflow as tf
from tensorflow.keras.preprocessing import image  # Для работы с изображениями 
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.applications import EfficientNetB0
from keras.applications.imagenet_utils import decode_predictions  # Для декодирования лейблов
from tensorflow.keras.applications import 
'''


def get_date_ajax(SITE):
    answer = {'answer': 'success'}
    return {'ajax': json.dumps(answer)}