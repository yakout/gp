'''
Usage : python labels_combiner.py [FOLDER_NAME] [OUT_NAME]
FOLDER_NAME : path of the folder that contains label files for
Output File Name = OUT_NAME
'''
import sys
import os, fnmatch
import numpy as np

def load_labels(file_path):
    labels = []
    with open(file_path) as f:
        for line in f: # read rest of lines
            labels.append(int(line))
    return labels


if (len(sys.argv) != 3):
    print("Invalid number of arguments: please add TWO arguments\nFOLDER_NAME + OUT_NAME")
    sys.exit()


folder_path = sys.argv[1]
output_file_name = sys.argv[2]

all_labels = []

list_of_files = os.listdir(folder_path)
pattern = "*.txt"
all_data = None
for entry in list_of_files:
    if fnmatch.fnmatch(entry, pattern):
        all_labels.append(load_labels(folder_path + entry))

all_labels = np.array(all_labels)

if len(all_labels) == 0:
    print("Empty Directory")
    sys.exit()

means = all_labels.mean(axis=0)
positives = means >= 0.5
negatives = means < 0.5
means[positives] = 1
means[negatives] = 0

np.savetxt(output_file_name + ".ht", means, delimiter='\n', fmt='%d')
