# 测试程序: CNN模型/FCNN模型实现对手写英文大小写字母的识别

# 测试集文件见 *data/letters_testset/* , 其中子文件夹名为标签
# 测试集大小为3700，其中每类字符100个数据

# 直接运行本程序, CNN模型对手写英文大小写字母精度达到92%左右


import argparse
import cv2
import imghdr
import numpy as np
import os
import pathlib
import pickle

from halo import Halo
from sklearn.model_selection import train_test_split
from keras.utils.np_utils import to_categorical
from keras import models, layers, regularizers
from tensorflow import optimizers


class Model:
    def __init__(self, data_dir_path: str = '', skip_evaluation: bool = False):
        self.skip_evaluation = skip_evaluation
        self.data_dir_path = data_dir_path

        if not (self.data_dir_path and self.data_dir_path.strip()):
            self.data_dir_path = '../data/letters_testset/'

    def read_dataset(self):
        """
        Method to read image dataset in numpy array for training the model.

        The structure of the EMNIST dir at `data_dir_path` should be:
            EMNIST
            ├── a
            |   ├── 1.png
            |   ├── 2.png
            |   └── ...
            ├── b
            |   ├── 1.png
            |   ├── 2.png
            |   └── ...
            └── ...

        Sub directory name is the name of the label and contains MNIST format compliant handwritten images
        of the character denoted by that label.
        """

        base_sep_count = self.data_dir_path.count(os.sep)
        features = []
        labels = []

        spinner = Halo(text='Reading', spinner='dots')
        spinner.start()

        for subdir, dirs, files in os.walk(self.data_dir_path, topdown=True):
            # go only 2 levels deep
            if subdir.count(os.sep) - base_sep_count == 1:
                del dirs[:]
                continue

            for filename in files:
                filepath = os.path.join(subdir, filename)

                if imghdr.what(filepath) == 'png':
                    labels.append([os.path.basename(os.path.dirname(filepath))])

                    name_im = cv2.imread(filename=filepath)
                    name_im = np.dot(name_im[..., :3], [0.299, 0.587, 0.114])
                    features.append(list(name_im))

        spinner.succeed(text='Finished reading')

        features = np.array(features)
        labels = np.array(labels).ravel()

        return features, labels


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""
            Script to train a kNN Classifier model.
            """,
        usage='%(prog)s [options]',
    )
    parser.add_argument(
        '-dap',
        '--EMNIST-path',
        dest='data_path',
        type=str,
        help='Path where dataset images are saved.',
    )
    parser.add_argument(
        '-se',
        '--skip-evaluation',
        dest='skip_evaluation',
        action='store_true',
        default=False,
        help='Whether to skip running evaluations or not.',
    )
    args = parser.parse_args()

    model = Model(data_dir_path=args.data_path, skip_evaluation=args.skip_evaluation)

    # 导入数据集
    x, y = model.read_dataset()
    # 变换数据的形状，将数据类型由uint8转为float32，归一化
    x_test_1 = x.reshape((3700, 28, 28, 1)).astype('float32') / 255
    x_test_2 = x.reshape((3700, 28 * 28)).astype('float32') / 255
    # one-hot编码形式
    y_test_1 = to_categorical(y)
    y_test_2 = to_categorical(y)

    # 导入cnn模型，在测试集上测试模型性能
    cnn_model = models.load_model('../model/cnn_letter_model.h5')
    loss, acc = cnn_model.evaluate(x_test_1, y_test_1)
    print('cnn_loss {}, cnn_acc {}'.format(loss, acc))

    # 导入fcnn模型，在测试集上测试模型性能
    fcnn_model = models.load_model('../model/fcnn_letter_model.h5')
    loss, acc = fcnn_model.evaluate(x_test_2, y_test_2)
    print('fcnn_loss {}, fcnn_acc {}'.format(loss, acc))
