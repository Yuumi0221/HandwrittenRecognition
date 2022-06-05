#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from keras.datasets import mnist
from keras import models
from keras import layers
from keras.utils.np_utils import to_categorical
import matplotlib.pyplot as plt

# 定义模型
def model_conv():
    model = models.Sequential()
    model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(36, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    # model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['acc'])
    return model

# 导入MNIST数据集
(train_data, train_labels), (test_data, test_labels) = mnist.load_data()
# print('train_shape {} {}'.format(train_data.shape, train_labels.shape))
# print('test_shape {} {}'.format(test_data.shape, test_labels.shape))
# plt.imshow(train_data[0])
# plt.title('number {}'.format(train_labels[0]))
# plt.show()

# 数据预处理
x_train = train_data.reshape((60000, 28, 28, 1)).astype('float32') / 255
x_test = test_data.reshape((10000, 28, 28, 1)).astype('float32') / 255
y_train = to_categorical(train_labels)
y_test = to_categorical(test_labels)
print(x_train.shape, y_train.shape)

# 定义模型
model = model_conv()
print(model.summary())

# 开始训练
# model.fit(x_train, y_train, epochs=5, batch_size=64, validation_split=0.1)
model.fit(x_train, y_train, epochs=10, batch_size=64, validation_split=0.1)

# 在测试集上测试模型性能
loss, acc = model.evaluate(x_test, y_test)
print('loss {}, acc {}'.format(loss, acc))

# 保存模型
model.save("../model/cnn_num_model.h5")
