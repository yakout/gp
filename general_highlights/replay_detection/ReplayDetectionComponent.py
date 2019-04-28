import numpy as np
from keras.models import load_model

import os, sys
sys.path.append(os.getcwd() + '/general_highlights/replay_detection/video_processing/model_trainer/')
from lk_track import FeaturesExtractor

sys.path.append("../..")
from video_model import Highlight, Chunk
from component import Component, ComponentContainer

model_location = os.getcwd() + "/general_highlights/replay_detection/video_processing/" + "model_trainer/replay_model.h5"

class ReplayDetectionComponent(Component):
    """
    This is an abstract class that any new highlight generator component should extend.

    Attributes:
        - model : DL model to use for classification to whether chunks are considered
        replay or note.
        - video_offset : frames offset in video.
    """
    def __init__ (self):
        ComponentContainer.register_component(ReplayDetectionComponent.get_name(), self)
        self.model = load_model(model_location)
        self.video_offset = 0

    @staticmethod
    def get_name():
        return 'replay_detection'

    def get_highlights(self, chunk: Chunk) -> 'List[Highlight]':
        """
        Gets highlights for this video chunk as per this component's perspective.
        :param chunk: the current video chunk being processed
        :return: list of highlights from given chunk
        """
        highlight = []
        features = FeaturesExtractor(chunk).run()
        # print("\t\t" + str(np.array(features).shape))
        features = np.array(features).reshape((1,2))
        prediction = self.model.predict(features)
        if (prediction[0] > 0.6):
            highlight.append(Highlight(self.video_offset, self.video_offset +
                        chunk.get_frames_count(), 1))
        self.video_offset += chunk.get_frames_count()
        return highlight
