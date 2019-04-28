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

import sys
sys.path.append("../../../../")
from video_model import Chunk
from video_processing import VideoChunkReader

from FeaturesExtractor import FeaturesExtractor

class FrameDifferenceFeature(FeaturesExtractor):
    def __init__(self, video_chunk):
        self.chunk = video_chunk

    def run(self):
        df = 0
        last_frame = 0
        for frame in self.chunk.get_clip().iter_frames():
            img = cv2.cvtColor(frame,cv2.COLOR_RGB2Luv)
            if(last_frame != 0):
                df.append(np.sum(np.abs(frame-last_frame)))

            last_frame = frame   

        return np.mean(df), zc.getZeroCrossingTheta_pzc(df)

def main():
    # import sys
#    try:
#        video_src = sys.argv[1]
#    except:
#        video_src = 0
    # sys.path.append("../../../")
    v = FeaturesExtractor("/home/ahmednagga19/Desktop/GP/gp/general_highlights/replay_detection/video_processing/videos/liv-cry-4-3.mp4").run()


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()