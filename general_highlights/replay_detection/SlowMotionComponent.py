import sys
import cv2
import numpy as np
from general_highlights.replay_detection import config
from general_highlights.replay_detection import constant
from numpy import linalg as LA
from general_highlights.replay_detection import ZeroCrossing as zc


from abc import ABC, abstractmethod
from typing import List, Mapping

sys.path.append("../..")
from video_model import Highlight, Chunk
from component import Component, ComponentContainer

class SlowMotionComponent(Component):
    """
    This is an abstract class that any new highlight generator component should extend.
    """
    def __init__ (self):
        ComponentContainer.register_component(SlowMotionComponent.get_name(), self)

    @staticmethod
    def get_name():
        return 'slow_motion'

    @abstractmethod
    def get_highlights(self, chunk: Chunk) -> 'List[Highlight]':
        """
        Gets highlights for this video chunk as per this component's perspective.
        :param chunk: the current video chunk being processed
        :return: list of highlights from given chunk
        """
        highlights = []
        # Read two frames, last and current, and convert current to gray.
        last_frame = chunk.get_frame(0)

        width, height, depth = last_frame.shape
        size = width*height*depth
        frames_count = 1
        window_count = 0
        window = []

        negro_window = []
        for current_frame in chunk.get_frames():
            # We want two frames- last and current, so that we can calculate the different between them.
            # Store the current frame as last_frame, and then read a new one
            gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

            # Find the absolute difference between frames
            d = LA.norm(cv2.absdiff(last_frame, current_frame))/size

            # print(d)
            window.append(d)
            if(frames_count%constant.WINDOW_SIZE == 0):
                window_count += 1
                print("New Window", window_count)
                print("mean" , np.mean(window))
                print("median" , np.median(window))
                print("variance", np.var(window))
                score = zc.getZeroCrossingTheta_pzc(len(window)-1, window)
                if(np.mean(window) < .002 and score > 10):
                    highlights.append(Highlight(frames_count, frames_count-len(window)+1, score/100))
                window = []

            last_frame = current_frame
            print(zc.getZeroCrossingTheta_pzc(frames_count, window))
            frames_count += 1
            # cv2.imshow('Video',current_frame)


            return highlights
