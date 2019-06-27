import sys
import os
import numpy as np
import glob
import pickle  # for model persistence
import platform  # To check if windows or linux for file paths
import threading
import time

from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, StratifiedShuffleSplit

class AudioClassifier:
    # pos_path is the path for .npy files that contains positive samples
    # neg_path is the path for .npy files that contains negative samples
    def __init__(self, training_lock):
        self.clf = None
        self.features_path = 'training_data/features'
        self.data_path = 'training_data/data'
        self.train_data_path = 'training_data'
        self.training_lock = training_lock

        self.model_file_name = 'svm_model.pickle'
        if os.path.isfile(self.model_file_name):
            print("Model exist, loading ...")
            self.load() # load and set the classifier
        else:
            # For training

            # We need to aquire the training lock so only one worker is training
            # and other workers will be blocked until lock is release i.e training
            # is done.
            with self.training_lock:
                if os.path.isfile(self.model_file_name):
                    print("Model exist, loading ...")
                    self.load() # load and set the classifier
                else:
                    print("No model exist, Training the sound model ...")
                    start = time.time()
                    self.extract_features()
                    self.prepare_data()
                    self.fit() # train and set the classifier
                    end = time.time()
                    print("Sound model training time: {} mins".format((end - start) / 60))

    def extract_features(self):
        print("Extracting features from data ..")

        self._generate_train_data_txt()

        os.makedirs(self.features_path + '/pos', exist_ok=True)
        os.makedirs(self.features_path + '/neg', exist_ok=True)

        os.system("python SoundNet-tensorflow/extract_feat.py -m 17 -x 18 -s -p extract -t {} --outpath {}".format(
            self.train_data_path + '/train_data_pos.txt',
            self.features_path + '/pos')
            )

        os.system("python SoundNet-tensorflow/extract_feat.py -m 17 -x 18 -s -p extract -t {} --outpath {}".format(
            self.train_data_path + '/train_data_neg.txt',
            self.features_path + '/neg')
            )

    # This will read the sample from paths and prepare them to the model to fit.
    def prepare_data(self):
        print("Preparing training data ..")

        X_all = []
        y_all = []

        # positive samples
        for _, file in enumerate(glob.glob(self.features_path + '/pos/*.npy')):
            #   print(np.load(file).shape)
            X_all.append(np.load(file).reshape(-1))
            y_all.append(1)

        # negative samples
        for _, file in enumerate(glob.glob(self.features_path + '/neg/*.npy')):
            X_all.append(np.load(file).reshape(-1))
            y_all.append(0)

        X_all = np.array(X_all)
        y_all = np.array(y_all)

        X_train, X_test, y_train, y_test = train_test_split(X_all,
                                                            y_all,
                                                            test_size=0.2,
                                                            random_state=42)
        self.X_train = X_all
        self.y_train = y_all
        self.X_test = X_test
        self.y_test = y_test

    def fit(self, random_state=0, tol=1e-5, C=0.01):
        # The Stratified ShuffleSplit cross-validator object is a merge of
        # StratifiedKFold and ShuffleSplit, which returns stratified randomized
        # folds.
        # The folds are made by preserving the percentage of samples for each
        # class.
        skf = StratifiedShuffleSplit() # by default n_splits=10
        best_score = 0

        for train_index, test_index in skf.split(self.X_train, self.y_train):
            X_train, X_test = self.X_train[train_index], self.X_train[test_index]
            y_train, y_test = self.y_train[train_index], self.y_train[test_index]
            clf = SVC(kernel='linear',
                      random_state=random_state,
                      tol=tol,
                      C=C,
                      probability=True)
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)
            if score > best_score:
                best_score = score
                self.clf = clf

        print("cross validation best score: {}".format(best_score))
        print("Model Score: {}".format(clf.score(self.X_test, self.y_test)))

        # persist model
        with open(self.model_file_name, 'wb') as handle:
            # The advantage of HIGHEST_PROTOCOL is that files get smaller.
            # This makes unpickling sometimes much faster.
            pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # this will load pretrainded model from given path, or from default path
    def load(self):
        with open(self.model_file_name, 'rb') as handle:
            self.clf = pickle.load(handle)

    def predict(self, data_path):
        X_data = []
        files = glob.glob(data_path + '/*.npy')
        # file: ./test_output_2/383.npy
        if platform.system() == 'Windows':
            files = sorted(files, key=lambda file: int(
                file.split('\\')[-1].split('.')[0]))
        else:
            files = sorted(files, key=lambda file: int(
                file.split('/')[-1].split('.')[0]))
        shape = np.load(files[0]).shape
        for _, file in enumerate(files):
            arr = np.load(file)
            if arr.shape != shape:
                print("Corrupted file {}".format(file))
                continue
            X_data.append(arr.reshape(-1))

        X_data = np.array(X_data)

        return self.clf.predict_proba(X_data)

    def _generate_train_data_txt(self):
        with open(self.train_data_path + "/train_data_{}.txt".format('pos'), 'w') as handle:
            files = glob.glob(self.data_path + '/pos/*.mp3')
            for file in files:
                handle.write(file)
                handle.write('\n')

        with open(self.train_data_path + "/train_data_{}.txt".format('neg'), 'w') as handle:
            files = glob.glob(self.data_path + '/neg/*.mp3')
            for file in files:
                handle.write(file)
                handle.write('\n')
