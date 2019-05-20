import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import Adam


from sklearn.model_selection import train_test_split
from utils import DatasetReader

class Trainer:
    """
        A class to train a model on data given dataset directory.

        The class does the following :
            1- loads data using DatasetReader from utils.py.
            2- partitions the data into train/dev/test partitions
            3- train the model
            4- Save the model by Pickle

        Attributes :
            - all_data : all the data for learning available as read from the
            train_data folder
            - means : train_data means for normalization on test
            - do_save_model : boolean to state whether to save the model files after training

        Methods :
            - read_data : reads all_data from train_data folder
            - partition_dataset : partitions data into train/dev/test splits
            -  create_model : creates the DL model
            - train : trains the model and save it if needed
            - save_model : save model to disk

        Local Dependencies :
            1- DatasetReader from utils.py

        Dependencies :
            1- numpy
            2- Keras
            3- Pickle
    """
    def __init__(self, dataset_dir, do_save_model=False):
        self.all_data = self.read_data(dataset_dir)
        self.do_save_model = do_save_model
        self.means = None
        self.std = None
        self.preprocess_data()
        if (self.means is None or self.std is None):
            print("ERROR : Means still = None")

    def read_data(self, dataset_dir):
        reader = DatasetReader(dataset_dir)
        return reader.read_data()

    def fill_nans(self):
        nan_means = np.nanmean(self.all_data, axis=0)
        nan_indices = np.argwhere(np.isnan(self.all_data))
        for nan_index in nan_indices:
            i, j = nan_index[0], nan_index[1]
            self.all_data[i,j] = nan_means[j]

    def normalize(self):
        self.means = self.all_data.mean(axis=0)
        self.std = self.all_data.std(axis=0)
        self.all_data[:, :-1] -= self.means[:-1]
        self.all_data[:, :-1] /= self.std[:-1]

    def down_sample_zero_labels(self):
        labels = self.all_data[:, -1]
        labels = labels.reshape((labels.shape[0], 1))
        zero_label_index = np.where(labels == 0)[0]
        one_label_index = np.where(labels == 1)[0]
        if (len(zero_label_index) > len(one_label_index)):
            zero_label_index = zero_label_index[:len(one_label_index) + 1]
        zero_label_data = self.all_data[zero_label_index]
        self.all_data = np.vstack((zero_label_data, self.all_data[one_label_index]))

    def preprocess_data(self):
        self.fill_nans()
        self.normalize()
        self.down_sample_zero_labels()

    def partition_dataset(self):
        X = self.all_data[:, :-1]
        y = self.all_data[:, -1]
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                test_size=0.1, random_state=42)
        X_dev, X_test, y_dev, y_test = train_test_split(X_test, y_test,
                test_size=0.5, random_state=42)
        return X_train, X_dev, X_test, y_train, y_dev, y_test

    def create_model(self):
        # Model Architecture
        model = Sequential()
        model.add(Dense(128, input_shape=(self.all_data.shape[1] - 1,), activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(128, activation='relu'))
        # model.add(Dropout(0.3))
        # model.add(Dense(128, activation='relu'))
        # model.add(Dropout(0.5))
        # model.add(Dense(128, activation='relu'))
        # model.add(Dropout(0.6))
        # model.add(Dense(128, activation='relu'))
        # model.add(Dropout(0.6))
        # model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.8))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.7))
        model.add(Dense(32, activation='relu'))
        # model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
        # Model Config
        model.compile(optimizer=Adam(lr=0.00005),
              loss='binary_crossentropy',
              metrics=['accuracy'])
        return model

    def save_model(self, model):
        model.save('replay_model.h5')
        np.save('means', self.means)
        np.save('stds', self.std)



    def train(self):
        print("Dataset Shape : ")
        print((self.all_data.shape))
        # shuffle to remove Dependencies in consective scenes
        np.random.shuffle(self.all_data)
        # partition data to train/dev/test
        X_train, X_dev, X_test, y_train, y_dev, y_test = self.partition_dataset()
        # ceate and train model
        model = self.create_model()
        model.fit(X_train, y_train,  validation_data=(X_dev, y_dev), epochs=100)
        print(model.evaluate(X_test, y_test))
        if (self.do_save_model):
            self.save_model(model)

if __name__ == '__main__':
    trainer = Trainer("./train_data/", do_save_model=True)
    trainer.train()
