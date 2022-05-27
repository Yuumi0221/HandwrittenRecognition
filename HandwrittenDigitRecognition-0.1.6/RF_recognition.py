import cv2
import numpy as np
from PIL import Image
import pickle


# 反相灰度图，将黑白阈值颠倒
def accessPiexl(img):
    height = img.shape[0]
    width = img.shape[1]
    for i in range(height):
        for j in range(width):
            img[i][j] = 255 - img[i][j]
    return img

# 反相二值化图像
def accessBinary(img, threshold=128):
    img = accessPiexl(img)
    # 边缘膨胀，不加也可以
    kernel = np.ones((3, 3), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    _, img = cv2.threshold(img, threshold, 0, cv2.THRESH_TOZERO)
    return img

# 根据长向量找出顶点
def extractPeek(array_vals, min_vals=10, min_rect=20):
    extrackPoints = []
    startPoint = None
    endPoint = None
    for i, point in enumerate(array_vals):
        if point > min_vals and startPoint == None:
            startPoint = i
        elif point < min_vals and startPoint != None:
            endPoint = i

        if startPoint != None and endPoint != None:
            extrackPoints.append((startPoint, endPoint))
            startPoint = None
            endPoint = None

    # 剔除噪点
    for point in extrackPoints:
        if point[1] - point[0] < min_rect:
            extrackPoints.remove(point)
    return extrackPoints

# 寻找边缘，返回边框的左上角和右下角（利用直方图寻找边缘算法（需行对齐））
def findBorderHistogram(path):
    borders = []
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = accessBinary(img)
    # 行扫描
    hori_vals = np.sum(img, axis=1)
    hori_points = extractPeek(hori_vals)
    # 根据每一行来扫描列
    for hori_point in hori_points:
        extractImg = img[hori_point[0]:hori_point[1], :]
        vec_vals = np.sum(extractImg, axis=0)
        vec_points = extractPeek(vec_vals, min_rect=0)
        for vect_point in vec_points:
            border = [(vect_point[0], hori_point[0]), (vect_point[1], hori_point[1])]
            borders.append(border)
    return borders

# 根据边框转换为MNIST格式
def transMNIST(path, borders, size=(28, 28)):
    # imgData = np.zeros((len(borders), size[0], size[0], 1), dtype='uint8')
    imgData = np.zeros((len(borders), size[0], size[0]), dtype='uint8')
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = accessBinary(img)
    for i, border in enumerate(borders):
        borderImg = img[border[0][1]:border[1][1], border[0][0]:border[1][0]]
        # 根据最大边缘拓展像素
        extendPiexl = (max(borderImg.shape) - min(borderImg.shape)) // 2
        targetImg = cv2.copyMakeBorder(borderImg, 7, 7, extendPiexl + 7, extendPiexl + 7, cv2.BORDER_CONSTANT)
        targetImg = cv2.resize(targetImg, size)
        # targetImg = np.expand_dims(targetImg, axis=-1)
        imgData[i] = targetImg
    return imgData

# 预测手写多字符
def multi_predict(modelpath, imgPath):
    borders = findBorderHistogram(imgPath)
    imgData = transMNIST(imgPath, borders)

    # 导入模型
    with open(modelpath, 'rb') as f:
        rf_model = pickle.load(f)
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
        img_pre = rf_model.predict(img)
        result_number.append(int(img_pre))

    result_numberToString = ''.join([str(x) for x in result_number])
    return result_numberToString

# 预测手写单字符
def single_predict(modelpath, imgPath):
    # 图片预处理
    img = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    img = accessBinary(img)
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
        rf_model = pickle.load(f)
    # 预测结果
    img_pre = rf_model.predict(img)
    return int(img_pre)

# # 测试代码
# model = 'model/RF_model.pkl'
# path = 'imgs/99.png'
# result = single_predict(model, path)
# print("识别结果是:", result)
