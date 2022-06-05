# -*- coding: utf-8 -*-
import cv2
import numpy as np
import tool as tl
from keras import models
import tensorflow as tf


# 预测手写多字符
# def multi_predict(modelpath, imgData):
def multi_predict(modelpath, imgPath):
    # borders = findBorderContours(path)
    borders = tl.findBorderHistogram(imgPath)
    imgData = tl.cnn_transMNIST(imgPath, borders)
    # 图片数据归一化
    img = imgData.astype('float32') / 255
    # 导入模型
    cnn_model = models.load_model(modelpath)
    # print(model.summary())
    # 预测结果
    results = cnn_model.predict(img)
    result_number = []
    for result in results:
        result_number.append(np.argmax(result))
    result_numberToString = ''.join([str(x) for x in result_number])
    return result_numberToString


# 预测手写单字符
def single_predict(modelpath, imgPath):
    # 图片预处理
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    # cv2.imshow('test', img)
    # cv2.waitKey(0)
    img = tl.accessBinary(img)
    img = cv2.resize(img, (28, 28))
    img = img / 255.0
    # 扩展维度
    # img = img[tf.newaxis, ...]
    img = np.expand_dims(img, axis=0)

    # 导入模型
    cnn_model = models.load_model(modelpath)
    # 预测结果
    img_pre = cnn_model.predict(img)
    img_pre = tf.argmax(img_pre, axis=1)
    result = np.array(img_pre)[0]
    return result

# # 测试代码
# path = '../imgs/test2.jpg'
# model = '../model/cnn_num_model.h5'
#
# multi_char = 1
#
# # 多字符
# if multi_char == 1:
#     results = multi_predict(model, path)
#     print("识别结果是:", results)
#     # showResults(path, borders, results)
# # 单字符
# else:
#     result = single_predict(model, path)
#     print("识别结果是:", result)
