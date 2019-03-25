import numpy as np
import glob
import pickle  # for model persistence
import platform  # To check if windows or linux for file paths

from sklearn.svm import SVC
from sklearn.model_selection import cross_validate, train_test_split, StratifiedShuffleSplit


class AudioClassifier:
    # pos_path is the path for .npy files that contains positive samples
    # neg_path is the path for .npy files that contains negative samples
    def __init__(self, pos_path=None, neg_path=None):
        self.pos_path = pos_path
        self.neg_path = neg_path
        self.clf = None
        self.model_file_name = 'svm_model.pickle'
        if pos_path and neg_path:
            # for training
            self.prepare_data()
            self.fit()
        else:
            self.load()

    # This will read the sample from paths and prepare them to the model to fit.

    def prepare_data(self):
        X_all = []
        y_all = []

        for _, file in enumerate(glob.glob(self.pos_path + '/*.npy')):
            #   print(np.load(file).shape)
            X_all.append(np.load(file).reshape(-1))
            y_all.append(1)

        for _, file in enumerate(glob.glob(self.neg_path + '/*.npy')):
            X_all.append(np.load(file).reshape(-1))
            y_all.append(0)

        X_all = np.array(X_all)
        y_all = np.array(y_all)

        X_train, X_test, y_train, y_test = train_test_split(X_all,
                                                            y_all,
                                                            test_size=0.3,
                                                            random_state=42)
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def fit(self, random_state=0, tol=1e-5, C=0.01):
        clf = SVC(kernel='linear', random_state=random_state,
                  tol=tol, C=C, probability=True)
        clf.fit(self.X_train, self.y_train)
        self.clf = clf
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
        for i, file in enumerate(files):
            arr = np.load(file)
            if arr.shape != shape:
                print("corrupted file {}".format(file))
                continue
            X_data.append(arr.reshape(-1))

        X_data = np.array(X_data)

        return self.clf.predict_proba(X_data)
