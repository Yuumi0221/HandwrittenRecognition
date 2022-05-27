# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import CNN_recognition as cnn_rec
import KNN_recognition as knn_rec
import SVM_recognition as svm_rec
import FCNN_recognition as fcnn_rec
import RF_recognition as rf_rec
import tensorflow as tf
import cv2
from keras import models
import time

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="手写字符识别")


@app.get("/")
async def root():
    return {"message": "Hello world, FastAPI"}


@app.get("/v1/typeChange", summary="更改识别类型", tags=["识别类型"],
         description="model_type: 0:cnn 1:fcnn 2:knn 3:svm 4:rf")
async def recType(model_type: int, multi_char: int, num_letter: int):
    try:
        global modelType
        global multiChar
        global numLetter
        modelType = model_type
        multiChar = multi_char
        numLetter = num_letter

        if modelType == 0:
            modelName = 'CNN'
        elif modelType == 1:
            modelName = 'FCNN'
        elif modelType == 2:
            modelName = 'KNN'
        elif modelType == 3:
            modelName = 'SVM'
        elif modelType == 4:
            modelName = 'RF'

        data = {
            "code": 200,
            "msg": "修改类型成功",
            "model_type": modelType,
            "model_name": modelName,
            "multi_char": multiChar,
            "num_letter": numLetter
        }
        return JSONResponse(data)
    except Exception as e:
        return {"code": 201, "msg": "修改类型失败"}


@app.post("/v1/upload", summary="上传识别", tags=["上传"])
async def upload(file: UploadFile = File(...)):
    # 计算开始时间
    time1 = time.time()
    file_bytes = file.file.read()
    tempfile = 'imgs/temp.png'
    try:
        with open(tempfile, "wb") as f:
            f.write(file_bytes)
        result = recognition(tempfile, modelType, multiChar)
        if result == '':
            return {"code": 201, "msg": "上传失败"}
        # 计算结束时间
        time2 = time.time()
        data = {
            "code": 200,
            "msg": "上传成功",
            "result": result,
            "time": str(time2 - time1)
        }
        return JSONResponse(data)
    except Exception as e:
        return {"code": 201, "msg": "上传失败"}


def recognition(path, model_type, multi_char):
    # cnn
    if model_type == 0:
        model = 'model/cnn_model.h5'
        # print('CNN算法')
        # 多字符
        if multi_char == 1:
            print("CNN算法识别多字符数字...")
            result = cnn_rec.multi_predict(model, path)
            print("识别结果:", result)
        # 单字符
        else:
            print("CNN算法识别单字符数字...")
            result = cnn_rec.single_predict(model, path)
            print("识别结果:", result)

    # fcnn
    elif model_type == 1:
        model = 'model/fcnn_model.h5'
        if multi_char == 1:
            print("FCNN算法识别多字符数字...")
            result = fcnn_rec.multi_predict(model, path)
            print("识别结果:", result)
        else:
            print("FCNN算法识别单字符数字...")
            result = fcnn_rec.single_predict(model, path)
            print("识别结果:", result)

    # knn
    elif model_type == 2:
        model = 'model/knn.pkl'
        if multi_char == 1:
            print("KNN算法识别多字符数字...")
            result = knn_rec.multi_predict(model, path)
            print("识别结果:", result)
        else:
            print("KNN算法识别单字符数字...")
            result = knn_rec.single_predict(model, path)
            print("识别结果:", result)

    # svm
    elif model_type == 3:
        model = 'model/svm_model.pkl'
        if multi_char == 1:
            print("SVM算法识别多字符数字...")
            result = svm_rec.multi_predict(model, path)
            print("识别结果:", result)
        else:
            print("SVM算法识别单字符数字...")
            result = svm_rec.single_predict(model, path)
            print("识别结果:", result)

    # rf
    elif model_type == 4:
        model = 'model/RF_model.pkl'
        if multi_char == 1:
            print("RandomForest算法识别多字符数字...")
            result = rf_rec.multi_predict(model, path)
            print("识别结果:", result)
        else:
            print("RandomForest算法识别单字符数字...")
            result = rf_rec.single_predict(model, path)
            print("识别结果:", result)

    return str(result)


# 连接手机
# if __name__ == '__main__':
#     uvicorn.run(app='main:app', host="192.168.1.100", port=5000, reload=True, debug=True)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=5000, reload=True, debug=True)
