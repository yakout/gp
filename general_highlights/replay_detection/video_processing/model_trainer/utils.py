import numpy as np
import os, fnmatch

class DatasetReader:
    '''
        Class to read dataset
    '''
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def read_data(self):
        listOfFiles = os.listdir(self.data_dir)
        pattern = "*.npy"
        all_data = None
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                file_path = self.data_dir + entry
                if all_data is None:
                    all_data = np.load(file_path)
                else:
                    all_data = np.concatenate((all_data, np.load(file_path)),
                        axis=0)
        return all_data
