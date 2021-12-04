import numpy as np
import matplotlib.pyplot as plt
import os, glob
import cv2

import eolearn
from eolearn.core import EOPatch, FeatureType

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras

# НАСТРОЙКИ
# Задаем целевой размер снимков
TARGET_SIZE = (64, 64)

# Гиперпараметры
# Использование в нейросети позиционного эмбэддинга
positional_emb = False

# Количество сверточных слоев в токенайзере
conv_layers = 2

# количество "голов" self-attention в блоках трансформера
num_heads = 2

# размер проэкционного канала
projection_dim = 128
# Размер блока трансформера
transformer_units = [
    projection_dim,
    projection_dim,
]
transformer_layers = 2
# уровень отключения слоев для stochastic depth
stochastic_depth_rate = 0.1

learning_rate = 0.001
batch_size = 128
num_epochs = 30
image_size = 64
input_shape = [64, 64, 19]


# Пример предсказания моделью розлива нефти
def example_prediction(SITE):
    '''
    Трансформер делит картинку на патчи - меньшие части, 
    анализирует их и дает им токены значения содержимого, 
    и токены значения позиции, а дальше работает как в нлп - анализирует, 
    как коррелируют значения содержимого каждого кусочка картинки с тем, 
    на каком месте эта часть картинки находится
    '''
    SITE.addHeadFile('/templates/system/js/html2pdf.bundle.js')
    SITE.addHeadFile('/templates/system/js/example_prediction.js')

    # Инициализация модели
    model = create_cct_model(input_shape = [64, 64, 19])
    model.summary()

    # оптимизатор и функция ошибки
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    model.compile(
        optimizer=optimizer,
        loss=keras.losses.BinaryCrossentropy(),
        metrics=[
            keras.metrics.Accuracy(name="accuracy")
        ],
    )

    # Загрузка весов модели
    model.load_weights('files/model/CCT.h5')

    # Для тестирования модели укажите свой idn папки (должна быть размещена на сервере)
    idn = '1000984c-8130-48cc-bedd-ba829a4f9c16'

    # путь к папке со снимками местности
    filepath = f'files/oil_pipelines/2021-01/{idn}/sentinel2-l2a/patches/64x64-10/2021'

    input_data = read_file(filepath)
    # Модель получила 28 снимков разных дат, выдала 28 предсказаний. 
    # Чем ближе к 1 - тем увереннее модель, что был разлив
    out = model(input_data, training=False)
    html = ''
    for i in range(out.shape[0]):
        html += f'<div>Снимок {i+1}, вероятность: {out[i, 0]}</div>'
    SITE.content = f'''
        <div id="pdf_out">
            <h1>Пример работы модели</h1>
            <div style="margin-bottom:20px;">Вероятность разлива для uid="{idn}" по снимкам за январь 2021 года</div>
            <div>{html}</div>
        </div>
        <div style="margin-top:20px;"><input id="pdf_button" class="dan_button_green" value="Сохранить в pdf"></div>
    '''


# Функция считывания файла
def read_file(filepath):
    '''
    Функция получает путь к папке содержащей файлы снимка
    и возвращает numpy-массив из совмещенных снимков по всем 19 (13 + 6, где 6 берём из папки 'mask') каналам
    '''
    eopatch = EOPatch.load(filepath)
    img = eopatch.data['L2A']
    masks = [eopatch.mask[x] for x in eopatch.mask]
    return np.concatenate([img] + masks, axis=-1)


# multilayer perceptron (MLP) для энкодера трансформера
def mlp(x, hidden_units, dropout_rate):
    '''
    Является надстройкой над блоком трансформера из последовательно расположенных 
    полносвязных слоев, для обработки фич, полученных от self-attention
    '''
    for units in hidden_units:
        x = layers.Dense(units, activation=tf.nn.gelu)(x)
        x = layers.Dropout(dropout_rate)(x)
    return x


# Финальная сборка модели
def create_cct_model(
    input_shape=input_shape,
    image_size=image_size,
    num_heads=num_heads,
    projection_dim=projection_dim,
    transformer_units=transformer_units,
):

    inputs = layers.Input(input_shape)

    # Кодирование (нарезка) патчей.
    cct_tokenizer = CCTTokenizer()
    encoded_patches = cct_tokenizer(inputs)

    # Применение позиционного эмбеддинга.
    
    # Stochastic Depth
    dpr = [x for x in np.linspace(0, stochastic_depth_rate, transformer_layers)]

    # Блоки трансформера.
    for i in range(transformer_layers):
        # Нормализация.
        x1 = layers.LayerNormalization(epsilon=1e-5)(encoded_patches)

        # Self-Attention-блок.
        attention_output = layers.MultiHeadAttention(
            num_heads=num_heads, key_dim=projection_dim, dropout=0.1
        )(x1, x1)

        # Skip-connection.
        attention_output = StochasticDepth(dpr[i])(attention_output)
        x2 = layers.Add()([attention_output, encoded_patches])

        # Нормализация.
        x3 = layers.LayerNormalization(epsilon=1e-5)(x2)

        # MLP.
        x3 = mlp(x3, hidden_units=transformer_units, dropout_rate=0.1)

        # Skip-connection.
        x3 = StochasticDepth(dpr[i])(x3)
        encoded_patches = layers.Add()([x3, x2])

    # Применение sequence pooling для получения взвешенного выхода сети.
    representation = layers.LayerNormalization(epsilon=1e-5)(encoded_patches)
    attention_weights = tf.nn.softmax(layers.Dense(1,)(representation), axis=1)
    weighted_representation = tf.matmul(
        attention_weights, representation, transpose_a=True
    )
    weighted_representation = tf.squeeze(weighted_representation, -2)

    # Выход классификатора.
    logits = layers.Dense(1,  activation='sigmoid')(weighted_representation)
    # Готовая модель
    model = keras.Model(inputs=inputs, outputs=logits)
    return model


# Токенайзер
class CCTTokenizer(layers.Layer):
    '''
    Токенизатор разбирает изображение на слои, для извлецения фич,
    затем растягивает их в двумерные вектора для работы с ними как с последовательностями
    '''
    def __init__(
        self,
        kernel_size=3,
        stride=1,
        padding=1,
        pooling_kernel_size=3,
        pooling_stride=2,
        num_conv_layers=conv_layers,
        num_output_channels=[64, 128],
        positional_emb=positional_emb,
        **kwargs,
    ):
        super(CCTTokenizer, self).__init__(**kwargs)

        self.conv_model = keras.Sequential()
        for i in range(num_conv_layers):
            self.conv_model.add(
                layers.Conv2D(
                    num_output_channels[i],
                    kernel_size,
                    stride,
                    padding="valid",
                    use_bias=False,
                    activation="relu",
                    kernel_initializer="he_normal",
                )
            )
            self.conv_model.add(layers.ZeroPadding2D(padding))
            self.conv_model.add(
                layers.MaxPool2D(pooling_kernel_size, pooling_stride, "same")
            )

        self.positional_emb = positional_emb

    def call(self, images):
        outputs = self.conv_model(images)
        # После прохождения данной мини-сетки изображение превращается в ряд последовательностей
        '''
        reshaped = tf.reshape(
            outputs,
            (-1, tf.shape(outputs)[1] * tf.shape(outputs)[2], tf.shape(outputs)[-1]),
        )
        '''
        reshaped = tf.reshape(
            outputs,
            (-1, outputs.shape[1] * outputs.shape[2], outputs.shape[-1]),
        )
        return reshaped

    def positional_embedding(self, image_size):
        # Опциональная часть с позиционным эмбеддингом
        if self.positional_emb:
            dummy_inputs = tf.ones((1, image_size, image_size, 3))
            dummy_outputs = self.call(dummy_inputs)
            sequence_length = tf.shape(dummy_outputs)[1]
            projection_dim = tf.shape(dummy_outputs)[-1]

            embed_layer = layers.Embedding(
                input_dim=sequence_length, output_dim=projection_dim
            )
            return embed_layer, sequence_length
        else:
            return None


# Stochastic depth
# Источник: github.com:rwightman/pytorch-image-models.
class StochasticDepth(layers.Layer):
    '''
    Stochastic depth - техника регуляризации, которая случайным образом блокирует 
    работу некоторых слоев нейросети. По смыслу близка к "дропауту" - Dropout, 
    с той разницей, что дропаут блокирует отдельные нейроны.
    '''
    def __init__(self, drop_prop, **kwargs):
        super(StochasticDepth, self).__init__(**kwargs)
        self.drop_prob = drop_prop

    def call(self, x, training=None):
        if training:
            keep_prob = 1 - self.drop_prob
            shape = (tf.shape(x)[0],) + (1,) * (len(tf.shape(x)) - 1)
            random_tensor = keep_prob + tf.random.uniform(shape, 0, 1)
            random_tensor = tf.floor(random_tensor)
            return (x / keep_prob) * random_tensor
        return x