# Importing all system components
import sys
from highlights_processing import Merger, Summarizer
from component import Chunk, Component, ComponentContainer
import cv2
import numpy as np
from numpy import linalg as LA
# from general_highlights.replay_detection import ZeroCrossing as zc
from SoundComponent import SoundComponent
from video_processing import VideoChunkReader


# Initially, game video is on disk

# Define constant of chunk here (something like 5/10 mins depending on the size of the video being loaded)

def init():
    """
      Initialize all needed structures(map of component confidence), constants, etc...
    """
    # {: 0.9, 'video': 0.5, }
    pass


if __name__ == "__main__":
    init()
    video_path = sys.argv[1]
    print(video_path)
    video_chunk_reader = VideoChunkReader(video_path)
    last_pos = 0
    all_highlights = {}
    st = SoundComponent.get_name()
    component_confidence_map = {SoundComponent.get_name(): 0.9}
    while (video_chunk_reader.has_next()):
        chunk = video_chunk_reader.get_next()
        highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
        all_highlights[chunk] = Merger.merge(highlghts_dict, component_confidence_map)

    # summarized_highights = Summarizer.summarize(all_highlights, duration_limit)

    # Output all_highlights
