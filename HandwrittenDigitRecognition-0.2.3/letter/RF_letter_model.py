import argparse
import cv2
import imghdr
import numpy as np
import os
import pathlib
import pickle

from halo import Halo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class Model:
    def __init__(self, data_dir_path: str = '', skip_evaluation: bool = False):
        self.skip_evaluation = skip_evaluation
        self.data_dir_path = data_dir_path

        if not (self.data_dir_path and self.data_dir_path.strip()):
            self.data_dir_path = '../data/EMNIST/'

        models_dir_path = os.path.abspath('../model/')
        pathlib.Path(models_dir_path).mkdir(parents=True, exist_ok=True)

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
                    name_im = name_im.flatten()
                    features.append(list(name_im))

        spinner.succeed(text='Finished reading')

        features = np.array(features)
        labels = np.array(labels).ravel()

        return features, labels


    def train(self):
        # 导入数据集
        x, y = self.read_dataset()
        # 变换数据的形状，将数据类型由uint8转为float32，归一化
        features_train, features_test, labels_train, labels_test = train_test_split(x, y, test_size=0.1, random_state=0)
        features_train = features_train.astype('float32') / 255
        features_test = features_test.astype('float32') / 255
        print('train_shape {} {}'.format(features_train.shape, labels_train.shape))
        print('test_shape {} {}'.format(features_test.shape, labels_test.shape))

        spinner = Halo(text='Training', spinner='dots')
        spinner.start()

        # 开始训练，传入模型的训练数据形状为(93240, 784) 训练标签为(93240,)
        model = RandomForestClassifier(n_estimators=50)
        model.fit(features_train, labels_train)

        spinner.succeed(text='Finished training')

        if self.skip_evaluation:
            print('Skipping running evaluation')

        else:
            spinner = Halo(text='Evaluating', spinner='dots')
            spinner.start()
            # 评估准确率
            score = model.score(features_test[:1000], labels_test[:1000])
            print('acc:', score)

            spinner.succeed(text='Finished evaluation')
            print(f'Accuracy (max=1.0): {score}')

        # 保存模型
        with open('../model/rf_letter_model.pkl', 'wb') as file:
            pickle.dump(model, file)

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
    model.train()