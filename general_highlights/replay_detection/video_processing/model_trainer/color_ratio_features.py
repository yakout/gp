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
from sklearn.mixture import GaussianMixture

import sys
sys.path.append("../../../../")
from video_model import Chunk
from video_processing import VideoChunkReader

from features_extractors import FeaturesExtractor

class ColorRatioFeatures(FeaturesExtractor):

    @staticmethod
    def get_name():
        return "ColorRatioFeatures"

    def __init__(self, video_chunk):
        self.chunk = video_chunk

    def dominantColors(self, img, K=5):

        #convert to rgb from bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #reshaping to a list of pixels
        Z = img.reshape((-1,3))
        Z = np.float32(Z)

        #using k-means to cluster pixels
        # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        # ret,labels,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
        gmm = GaussianMixture(n_components = K)
        gmm.fit(Z)
        labels = gmm.predict(Z)

        counts = []
        for i in range(K):
            counts.append(np.sum(np.where(labels == i)))

        #returning after converting to integer from float
        return counts

    def run(self):
        means = [0,0,0]
        K = 5
        for frame in self.chunk.get_clip().iter_frames():
            counts = self.dominantColors(frame)
            counts = sorted(counts)[K-3:]
            width, height, depth = frame.shape
            for i in range(3):
                means[i] += counts[i]/(width*height*depth)/self.chunk.get_frames_count()

        return means

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
