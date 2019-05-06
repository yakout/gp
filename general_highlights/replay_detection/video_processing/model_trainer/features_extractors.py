
from abc import ABC, abstractmethod


class FeaturesExtractor:
    """
    This is an abstract class that impemented by actual features exctrators get features.
    """

    @abstractmethod
    def run(self):
        """
        Gets features for this video chunk.
        :return: features
        """
        pass

class FeaturesExtractorComponent(FeaturesExtractor):
    """
    This is an abstract class that impemented by actual features exctrators get features.
    """
    features_extractors_dict = {}


    @staticmethod
    def register(features_extractor_name: str, features_extractor: FeaturesExtractor):
        """
        Registers the given component with the given name in the container.
                :param component_name: string representing the component name (must be unique for each component)
                :param component: Component object to be registered
        """
        FeaturesExtractorComponent.features_extractors_dict[features_extractor_name] = features_extractor

    def __init__ (self, video_chunk):
        self.chunk = video_chunk

    @abstractmethod
    def run(self):
        """
        Gets features for this video chunk.
        :return: features
        """
        features_vector = []
        for features_extractor_name, features_extractor in FeaturesExtractorComponent.features_extractors_dict.items():
            features_vector.extend(features_extractor(self.chunk).run())
        return features_vector
