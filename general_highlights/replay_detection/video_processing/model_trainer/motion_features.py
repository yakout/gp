#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py [<video_source>]


Keys
----
ESC - exit
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
from numpy import linalg as LA
import ZeroCrossing as zc
import moviepy.editor as mpe

import video
from common import anorm2, draw_str
from time import clock

import sys
sys.path.append("../../../../")
from features_extractors import FeaturesExtractor
from video_model import Chunk
from video_processing import VideoChunkReader
import matplotlib.pyplot as plt

lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
FEATURES_SIZE = 2

class MotionFeatures(FeaturesExtractor):

    @staticmethod
    def get_name():
        return "MotionFeatures"

    def __init__(self, video_chunk):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.chunk = video_chunk
        self.frame_idx = 0

    def run(self):
        mean_motion_vector = 0
        mean_number_of_tracks = 0
        motion_vectors = []
        number_of_tracks = []
        dm = []
        last_frame = None
        for frame in self.chunk.get_clip().iter_frames():
            frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            motion_vector = 0
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, _st, _err = cv.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, _st, _err = cv.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                diff = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    if(len(tr) > 0):
                        (pX, pY) = tr[-2]
                        motion_vector += (x-pX)*(x-pX) + (y-pY)*(y-pY)
                        if(not last_frame is None):
                            for i in range(-5,5):
                                x1 = int(x)+i
                                x2 = int(pX)+i
                                if(x1 < 0 or x2 < 0 or x1 >= frame.shape[0] or x2 >= last_frame.shape[0]):
                                    continue
                                for j in range(-5,5):
                                    y1 = int(y)+j
                                    y2 = int(pY)+j
                                    if(y1 < 0 or y2 < 0 or y1 >= frame[x1].shape[0] or y2 >= last_frame[x2].shape[0]):
                                        continue
                                    diff.append(np.abs(frame[x1,y1]-last_frame[x2,y2]))


                    new_tracks.append(tr)
                self.tracks = new_tracks
                dm.append(LA.norm(diff))
            mean_number_of_tracks += len(self.tracks)/self.chunk.get_frames_count()
            number_of_tracks.append(len(self.tracks))
            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv.circle(mask, (x, y), 5, 0, -1)
                p = cv.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            mean_motion_vector += motion_vector/self.chunk.get_frames_count()
            motion_vectors.append(motion_vector)

            self.frame_idx += 1
            self.prev_gray = frame_gray
            last_frame = frame


        #TO-DO dm might needs differen thetas in zero_crossing
        # print("motion features finished looping")
        # print([mean_motion_vector, mean_number_of_tracks, np.mean(dm), zc.getZeroCrossingTheta_pzc(dm)])

    
        return [mean_motion_vector, mean_number_of_tracks, np.mean(dm), zc.getZeroCrossingTheta_pzc(dm)]

def main():
    # import sys
#    try:
#        video_src = sys.argv[1]
#    except:
#        video_src = 0
    # sys.path.append("../../../")
    video_clip = mpe.VideoFileClip("/Users/ahmed/Desktop/GP/gp/general_highlights/replay_detection/video_processing/videos/Liverpool vs Porto 2 0 Goals and Highlights 2019 HD.mp4", verbose=True)
    v = MotionFeatures(Chunk(0, video_clip, 100, 100)).run()



if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()
