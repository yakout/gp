import numpy as np
from keras.models import load_model

import os, sys
sys.path.append(os.getcwd() + '/general_highlights/replay_detection/video_processing/model_trainer/')
from features_extractors import FeaturesExtractorComponent
from motion_features import MotionFeatures
from frame_difference_features import FrameDifferenceFeatures
from mean_coloring_features import MeanLUVColoringFeature

sys.path.append("../..")
from video_model import Highlight, Chunk
from component import Component, ComponentContainer

model_location = os.getcwd() + "/general_highlights/replay_detection/video_processing/" + "model_trainer/"
model_predictor_location = model_location + "replay_model.h5"
data_means_location = model_location + "means.npy"
data_std_location = model_location + "stds.npy"

class ReplayDetectionComponent(Component):
    """
    This is an abstract class that any new highlight generator component should extend.

    Attributes:
        - model : DL model to use for classification to whether chunks are considered
        replay or note.
        - means : train_data means for normalization
        - stds : train_data stds for normalization
        - video_offset : frames offset in video.
    """
    def __init__ (self):
        self.prepare_features_extractors()
        ComponentContainer.register_component(ReplayDetectionComponent.get_name(), self)
        self.model = load_model(model_predictor_location)
        self.means = np.load(data_means_location)
        self.stds = np.load(data_std_location)
        self.video_offset = 0

    @staticmethod
    def get_name():
        return 'replay_detection'

    def prepare_features_extractors(self):
        # Register needed features exctrators
        FeaturesExtractorComponent.register(MotionFeatures.get_name(),
                                            MotionFeatures)
        FeaturesExtractorComponent.register(MeanLUVColoringFeature.get_name(),
                                            MeanLUVColoringFeature)
        FeaturesExtractorComponent.register(FrameDifferenceFeatures.get_name(),
                                            FrameDifferenceFeatures)

    def fill_nans(self, data):
        nan_indices = np.argwhere(np.isnan(data))
        for nan_index in nan_indices:
            i, j = nan_index[0], nan_index[1]
            data[i,j] = self.means[j]
        return data

    def normalize(self, data):
        data -= self.means[:-1]
        data /= self.stds[:-1]
        return data

    def preprocess_data(self, data):
        data = self.fill_nans(data)
        data = self.normalize(data)
        return data

    def get_highlights(self, chunk: Chunk) -> 'List[Highlight]':
        """
        Gets highlights for this video chunk as per this component's perspective.
        :param chunk: the current video chunk being processed
        :return: list of highlights from given chunk
        """
        highlight = []
        features = FeaturesExtractorComponent(chunk).run()
        features = np.array(features).reshape((1,len(features)))
        prediction = self.model.predict(self.preprocess_data(features))
        if (prediction[0] > 0.5):
            highlight.append(Highlight(self.video_offset, self.video_offset +
                        chunk.get_frames_count(), 1))
        self.video_offset += chunk.get_frames_count()
        return highlight
