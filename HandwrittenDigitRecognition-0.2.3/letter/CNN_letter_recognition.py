import cv2
import numpy as np
from keras import models
import tensorflow as tf
import tool as tl


# 预测手写多字符
def multi_predict(modelpath, imgPath):
    borders = tl.findBorderHistogram(imgPath)
    imgData = tl.cnn_transMNIST(imgPath, borders)

    # 导入模型
    cnn_model = models.load_model(modelpath)
    result_letter = []

    for img in imgData:
        # 将数据类型由uint8转为float32
        img = img.astype(np.float32)
        # 图片数据归一化
        img = img / 255.0
        # 扩展维度
        # img = img[tf.newaxis, ...]
        img = np.expand_dims(img, axis=0)

        # 预测结果
        img_pre = cnn_model.predict(img)
        img_pre = tf.argmax(img_pre, axis=1)
        result = np.array(img_pre)[0]
        result_letter.append(tl.map[result])

    result_numberToString = ''.join(result_letter)
    return result_numberToString


# 预测手写单字符
def single_predict(modelpath, imgPath):
    # 图片预处理
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    img = tl.accessBinary(img)
    img = cv2.resize(img, (28, 28))
    # 将数据类型由uint8转为float32
    img = img.astype(np.float32)
    # 图片数据归一化
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
    return tl.map[result]

# # 测试代码
# model = '../model/cnn_letter_model.h5'
# path = '../imgs/AC.png'
# result = multi_predict(model, path)
# # result = single_predict(model, path)
# print('识别结果:', result)
