
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