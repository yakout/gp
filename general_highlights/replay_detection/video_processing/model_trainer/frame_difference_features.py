#!/usr/bin/env python

'''
FrameDifferenceFeatures.py
====================

This calls used for getting mean of frame differences in the shot and also
the zero_crossing value of those differences

Those features used for detecting slow motions
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import ZeroCrossing as zc
from numpy import linalg as LA
import moviepy.editor as mpe

import sys
sys.path.append("../../../../")
from video_model import Chunk
from video_processing import VideoChunkReader

from features_extractors import FeaturesExtractor

class FrameDifferenceFeatures(FeaturesExtractor):

    @staticmethod
    def get_name():
        return "FrameDifferenceFeatures"

    def __init__(self, video_chunk):
        self.chunk = video_chunk

    def run(self):
        df = []
        last_frame = None
        for frame in self.chunk.get_clip().iter_frames():
            if(not last_frame is None):
                width, height, depth = frame.shape
                d = LA.norm(cv2.absdiff(last_frame, frame))/(width*height*depth)
                df.append(d)
                # print(len(df), " ", d)
            last_frame = frame

        print("frame difference finished looping")
        print([np.mean(df), zc.getZeroCrossingTheta_pzc(df)])
        return [np.mean(df), zc.getZeroCrossingTheta_pzc(df)]

def main():
    # import sys
#    try:
#        video_src = sys.argv[1]
#    except:
#        video_src = 0
    # sys.path.append("../../../")
    video_clip = mpe.VideoFileClip("/Users/ahmed/Desktop/GP/gp/general_highlights/replay_detection/video_processing/videos/Liverpool vs Porto 2 0 Goals and Highlights 2019 HD.mp4", verbose=True)
    v = FrameDifferenceFeatures(Chunk(0, video_clip, 0, 0)).run()


if __name__ == '__main__':
    print(__doc__)
    main()
