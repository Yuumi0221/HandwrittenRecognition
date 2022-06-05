import cv2
import numpy as np
import tool as tl
import pickle


# 预测手写多字符
def multi_predict(modelpath, imgPath):
    borders = tl.findBorderHistogram(imgPath)
    imgData = tl.transMNIST(imgPath, borders)

    # 导入模型
    with open(modelpath, 'rb') as f:
        knn_model = pickle.load(f)
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
        img_pre = knn_model.predict(img)
        result_number.append(int(img_pre[0]))

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
    with open(modelpath, 'rb') as f:
        knn_model = pickle.load(f)
    # 预测结果
    img_pre = knn_model.predict(img)
    return int(img_pre[0])

# # 测试代码
# model = '../model/knn_num_model.pkl'
# path = '../imgs/1234.png'
# result = multi_predict(model, path)
# print("识别结果是:",  result)
