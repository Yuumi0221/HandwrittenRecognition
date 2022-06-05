from keras.utils.np_utils import to_categorical
from keras import models, layers, regularizers
from tensorflow import optimizers
from keras.datasets import mnist

# 定义模型
def model_fcnn():
    model = models.Sequential()
    model.add(layers.Dense(units=128, activation='relu', input_shape=(28*28, ),
                             kernel_regularizer=regularizers.l1(0.0001)))
    model.add(layers.Dropout(0.01))
    model.add(layers.Dense(units=32, activation='relu',
                             kernel_regularizer=regularizers.l1(0.0001)))
    model.add(layers.Dropout(0.01))
    model.add(layers.Dense(units=10, activation='softmax'))
    # 编译
    model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 导入MNIST数据集
(train_data, train_labels), (test_data, test_labels) = mnist.load_data()
# 数据预处理
x_train = train_data.reshape((60000, 28*28)).astype('float') / 255
x_test = test_data.reshape((10000, 28*28)).astype('float') / 255
y_train = to_categorical(train_labels)
y_test = to_categorical(test_labels)
print(x_train.shape, y_train.shape)

# 定义模型
model = model_fcnn()

# 开始训练
model.fit(x_train, y_train, epochs=15, batch_size=128, verbose=2)


# 在测试集上测试模型性能
loss, acc = model.evaluate(x_test, y_test)
print('loss {}, acc {}'.format(loss, acc))

# 保存模型
model.save("../model/fcnn_num_model.h5")