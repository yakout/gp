# Importing all system components
import sys
from highlights_processing import Merger, Summarizer
from component import Chunk, Component, ComponentContainer
import cv2
import numpy as np
from numpy import linalg as LA
# from general_highlights.replay_detection import ZeroCrossing as zc
from SoundComponent import SoundComponent
from video_processing import VideoChunkReader, HighlightsVideoWriter
from general_highlights.replay_detection.SlowMotionComponent import SlowMotionComponent

# Deactivating tensorflow warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def init():
    """
      Initialize all needed structures(map of component confidence), constants, etc...
    """
    # {: 0.9, 'video': 0.5, }

    # registering components
    SoundComponent()
    # SlowMotionComponent()


if __name__ == "__main__":
    # Initialize Components and Components' confidence map
    init()
    component_confidence_map = {
        SoundComponent.get_name(): 0.9,
        # SlowMotionComponent.get_name() : 0.9
    }

    # Initialize chunk reader
    # chunk_size = 3000
    video_path = sys.argv[1]
    video_chunk_reader = VideoChunkReader(video_path)

    duration_limit = 100000
    all_highlights = {}

    # Iterate over all video's chunks and get highlights
    while (video_chunk_reader.has_next()):
        chunk = video_chunk_reader.get_next()
        if chunk == None:
            break
        #print("Chunk audio length : " + str(len(chunk.get_audio())))
        highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
        #print("Highlghts dict {}".format(highlghts_dict))
        all_highlights[chunk.get_chunk_position()] = Merger.merge(
            highlghts_dict, component_confidence_map)
        # print(len(all_highlights[chunk.get_chunk_position()]))

    summarized_highights = Summarizer.summarize(all_highlights, duration_limit)
    print("Summarized_highights {}".format(summarized_highights))
    writer = HighlightsVideoWriter(video_path,
                                   "output.mp4",
                                   video_chunk_reader.get_video_info(),
                                   VideoChunkReader(video_path))

    writer.write_video(summarized_highights)
