
#!/usr/bin/env python

'''
MeanLUVColoringFeature.py
====================

This calls used for getting mean of LUV color which helps in
specifying the shot and number of objects in it according to
dominant colors in the frame

'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2

import sys
sys.path.append("../../../../")
from video_model import Chunk
from video_processing import VideoChunkReader

from features_extractors import FeaturesExtractor
import moviepy.editor as mpe
import matplotlib.pyplot as plt

class MeanLUVColoringFeature(FeaturesExtractor):

    @staticmethod
    def get_name():
        return "MeanLUVColoringFeature"

    def __init__(self, video_chunk):
        self.chunk = video_chunk

    def run(self):
        mean_LUV_coloring = np.zeros(3)
        LUV_coloring = []
        for frame in self.chunk.get_clip().iter_frames():
            img = cv2.cvtColor(frame,cv2.COLOR_RGB2Luv)
            #Adding mean of cur frame to global LUV mean


            LUV_coloring.append(np.mean(img, axis=(0,1)))
            mean_LUV_coloring += np.mean(img, axis=(0,1))/self.chunk.get_frames_count()

        return mean_LUV_coloring.tolist()

def main():
    # import sys
#    try:
#        video_src = sys.argv[1]
#    except:
#        video_src = 0
    # sys.path.append("../../../")
    video_clip = mpe.VideoFileClip("/Users/ahmed/Desktop/GP/gp/general_highlights/replay_detection/video_processing/videos/Liverpool vs Porto 2 0 Goals and Highlights 2019 HD.mp4", verbose=True)
    v = MeanLUVColoringFeature(Chunk(0, video_clip, 0, 0)).run()

if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
