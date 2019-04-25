from keras.models import load_model

from video_processing.model_trainer.lk_track import FeaturesExtractor

sys.path.append("../..")
from video_model import Highlight, Chunk
from component import Component, ComponentContainer

class ReplayDetectionComponent(Component):
    """
    This is an abstract class that any new highlight generator component should extend.
    """
    def __init__ (self):
        ComponentContainer.register_component(ReplayDetectionComponent.get_name(), self)
        self.model = load_model('./model_trainer/replay_model.h5')

    @staticmethod
    def get_name():
        return 'replay_detection'

    @abstractmethod
    def get_highlights(self, chunk: Chunk) -> 'List[Highlight]':
        """
        Gets highlights for this video chunk as per this component's perspective.
        :param chunk: the current video chunk being processed
        :return: list of highlights from given chunk
        """
        highlight = []
        features = FeaturesExtractor(chunk).run()
        prediction = model.predict(features)[0]
        if (prediction > 0.6):
            highlight.append(Highlight(0, chunk.get_frames_count(), 1))

        return highlight
