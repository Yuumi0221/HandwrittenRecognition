import cv2
import numpy as np
import tool as tl
from keras import models
import tensorflow as tf


# 预测手写多字符
def multi_predict(modelpath, imgPath):
    borders = tl.findBorderHistogram(imgPath)
    imgData = tl.transMNIST(imgPath, borders)

    # 导入模型
    fcnn_model = models.load_model(modelpath)
    result_number = []

    for img in imgData:
        # 将数据类型由uint8转为float32
        img = img.astype(np.float32)
        # 图片形状由(28,28)转为(784,)
        img = img.reshape(-1, )
        # 增加一个维度变为(1,784)
        img = img.reshape(1, -1)
        # 图片数据归一化
        img = img / 255.0

        # 预测结果
        img_pre = fcnn_model.predict(img)
        img_pre = tf.argmax(img_pre, axis=1)
        result_number.append(np.array(img_pre)[0])

    result_numberToString = ''.join([str(x) for x in result_number])
    return result_numberToString


# 预测手写单字符
def single_predict(modelpath, imgPath):
    # 图片预处理
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    img = tl.accessBinary(img)
    img = cv2.resize(img, (28, 28))
    # 将数据类型由uint8转为float32
    img = img.astype(np.float32)
    # 图片形状由(28,28)转为(784,)
    img = img.reshape(-1, )
    # 增加一个维度变为(1,784)
    img = img.reshape(1, -1)
    # 图片数据归一化
    img = img / 255.0

    # 导入模型
    fcnn_model = models.load_model(modelpath)
    # 预测结果
    img_pre = fcnn_model.predict(img)
    img_pre = tf.argmax(img_pre, axis=1)
    result = np.array(img_pre)[0]
    return result

# # 测试代码
# model = '../model/fcnn_num_model.h5'
# path = '../imgs/test1.jpg'
#
# multi_char = 1
#
# # 多字符
# if multi_char == 1:
#     results = multi_predict(model, path)
#     print("识别结果是:", results)
# # 单字符
# else:
#     result = single_predict(model, path)
#     print("识别结果是:", result)
