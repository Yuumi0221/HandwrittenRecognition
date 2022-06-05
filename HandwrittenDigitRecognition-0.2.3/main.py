# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

import number.CNN_num_recognition as cnn_num_rec
import number.KNN_num_recognition as knn_num_rec
import number.SVM_num_recognition as svm_num_rec
import number.FCNN_num_recognition as fcnn_num_rec
import number.RF_num_recognition as rf_num_rec

import letter.CNN_letter_recognition as cnn_let_rec
import letter.FCNN_letter_recognition as fcnn_let_rec
import letter.KNN_letter_recognition as knn_let_rec
import letter.SVM_letter_recognition as svm_let_rec
import letter.RF_letter_recognition as rf_let_rec

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


@app.get("/typeChange", summary="更改识别类型", tags=["识别类型"],
         description="model_type: 0:CNN 1:FCNN 2:KNN 3:SVM 4:RF \r\n"
                     "multi_char: 0:单字符 1:多字符 \r\n"
                     "num_letter: 0:数字 1:字母")
async def typeChange(model_type: int, multi_char: int, num_letter: int):
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


@app.post("/upload", summary="上传识别", tags=["上传"])
async def upload(file: UploadFile = File(...)):
    # 计算开始时间
    time1 = time.time()
    file_bytes = file.file.read()
    tempfile = 'imgs/temp.png'
    try:
        with open(tempfile, "wb") as f:
            f.write(file_bytes)
        result = recognition(tempfile, numLetter, modelType, multiChar)
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


def recognition(path, num_letter, model_type, multi_char):
    # 识别数字
    if num_letter == 0:
        # cnn
        if model_type == 0:
            model = 'model/cnn_num_model.h5'
            # 多字符
            if multi_char == 1:
                print("CNN算法识别多字符数字...")
                result = cnn_num_rec.multi_predict(model, path)
                print("识别结果:", result)
            # 单字符
            else:
                print("CNN算法识别单字符数字...")
                result = cnn_num_rec.single_predict(model, path)
                print("识别结果:", result)

        # fcnn
        elif model_type == 1:
            model = 'model/fcnn_num_model.h5'
            if multi_char == 1:
                print("FCNN算法识别多字符数字...")
                result = fcnn_num_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("FCNN算法识别单字符数字...")
                result = fcnn_num_rec.single_predict(model, path)
                print("识别结果:", result)

        # knn
        elif model_type == 2:
            model = 'model/knn_num_model.pkl'
            if multi_char == 1:
                print("KNN算法识别多字符数字...")
                result = knn_num_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("KNN算法识别单字符数字...")
                result = knn_num_rec.single_predict(model, path)
                print("识别结果:", result)

        # svm
        elif model_type == 3:
            model = 'model/svm_num_model.pkl'
            if multi_char == 1:
                print("SVM算法识别多字符数字...")
                result = svm_num_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("SVM算法识别单字符数字...")
                result = svm_num_rec.single_predict(model, path)
                print("识别结果:", result)

        # rf
        elif model_type == 4:
            model = 'model/rf_num_model.pkl'
            if multi_char == 1:
                print("RandomForest算法识别多字符数字...")
                result = rf_num_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("RandomForest算法识别单字符数字...")
                result = rf_num_rec.single_predict(model, path)
                print("识别结果:", result)

    # 识别字母
    elif num_letter == 1:
        # cnn
        if model_type == 0:
            model = 'model/cnn_letter_model.h5'
            # 多字符
            if multi_char == 1:
                print("CNN算法识别多字符字母...")
                result = cnn_let_rec.multi_predict(model, path)
                print("识别结果:", result)
            # 单字符
            else:
                print("CNN算法识别单字符字母...")
                result = cnn_let_rec.single_predict(model, path)
                print("识别结果:", result)

        # fcnn
        elif model_type == 1:
            model = 'model/fcnn_letter_model.h5'
            if multi_char == 1:
                print("FCNN算法识别多字符字母...")
                result = fcnn_let_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("FCNN算法识别单字符字母...")
                result = fcnn_let_rec.single_predict(model, path)
                print("识别结果:", result)

        # knn
        if model_type == 2:
            model = 'model/knn_letter_model.pkl'
            if multi_char == 1:
                print("KNN算法识别多字符字母...")
                result = knn_let_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("KNN算法识别单字符字母...")
                result = knn_let_rec.single_predict(model, path)
                print("识别结果:", result)

        # svm
        elif model_type == 3:
            model = 'model/svm_letter_model.pkl'
            if multi_char == 1:
                print("SVM算法识别多字符字母...")
                result = svm_let_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("SVM算法识别单字符字母...")
                result = svm_let_rec.single_predict(model, path)
                print("识别结果:", result)

        # rf
        elif model_type == 4:
            model = 'model/rf_letter_model.pkl'
            if multi_char == 1:
                print("RandomForest算法识别多字符字母...")
                result = rf_let_rec.multi_predict(model, path)
                print("识别结果:", result)
            else:
                print("RandomForest算法识别单字符字母...")
                result = rf_let_rec.single_predict(model, path)
                print("识别结果:", result)

    return str(result)


# 连接手机
# if __name__ == '__main__':
#     uvicorn.run(app='main:app', host="192.168.1.113", port=5000, reload=True, debug=True)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=5000, reload=True, debug=True)
