import numpy as np
from keras.datasets import mnist
from keras import utils
from sklearn.ensemble import RandomForestClassifier
import pickle

# 导入MNIST数据集
(train_data, train_labels), (test_data, test_labels) = mnist.load_data()
# 变换数据的形状，将数据类型由uint8转为float32，归一化
x_train = train_data.reshape(train_data.shape[0], -1).astype('float32') / 255  # (60000, 784)
x_test = test_data.reshape(test_data.shape[0], -1).astype('float32') / 255
y_train = train_labels.astype(np.float32)
y_test = test_labels.astype(np.float32)

# 定义模型
model = RandomForestClassifier(n_estimators=100)
# 开始训练，传入模型的训练数据形状为(60000, 784) 训练标签为(60000,)
model.fit(x_train, y_train)
# 评估准确率
score = model.score(x_test, y_test)
print('acc:', score)
# 保存模型
with open('model/rf_model.pkl', 'wb') as file:
    pickle.dump(model, file)