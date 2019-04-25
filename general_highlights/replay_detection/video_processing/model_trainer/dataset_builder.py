VIDEO_DIR = "../videos/"
VIDEO_EXT = ".mp4"

TRAIN_DIR = "train_data/"
TRAIN_EXT = ".txt"

import numpy as np

# import lk_track as features_extractor
import sys
print(sys.path)
from lk_track import FeaturesExtractor

import sys
sys.path.append("../../../../")
from video_model import Chunk
from video_processing import VideoChunkReader
sys.path.append("general_highlights/replay_detection/video_processing/model_trainer/")

class DatasetBuilder:

    def __init__(self, videos_list):
        self.videos_list = videos_list

    def build_dataset(self):
        # process each video
        for video in self.videos_list:
            X = self.build_video_X(video)
            Y = self.build_video_Y(video)
            vidoe_data = np.column_stack((X, Y))
            np.save(TRAIN_DIR + video, vidoe_data)

    def build_video_X(self, video_name):
        video_features = []
        # extract features for each chunk in video
        vid_reader = VideoChunkReader(VIDEO_DIR + video_name + VIDEO_EXT, chunk_duration=0)
        counter = 0
        while vid_reader.has_next():
            chunk = vid_reader.get_next()
            # extract features for this chunks
            chunk_features = FeaturesExtractor(chunk).run()
            print("Finished " + str(counter))
            counter += 1
            # append to video_features
            video_features.append(chunk_features)
        # write features numpy array in file
        video_features = np.array(video_features)
        return video_features

    def build_video_Y(self, video_name):
        video_labels = []
        with open(TRAIN_DIR + video_name + TRAIN_EXT) as f:
            for line in f: # read rest of lines
                video_labels.append(int(line))
            video_labels = np.array(video_labels)
            return video_labels
        print("Error : no labels file for video name : " + video_name)

if __name__ == '__main__':
    videos_list = ['liv-cry-4-3']
    db = DatasetBuilder(videos_list)
    db.build_dataset()
