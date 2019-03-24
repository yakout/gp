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


# Initially, game video is on disk

# Define constant of chunk here (something like 5/10 mins depending on the size of the video being loaded)

def init():
    """
      Initialize all needed structures(map of component confidence), constants, etc...
    """
    # {: 0.9, 'video': 0.5, }

    # registering components
    # SoundComponent()
    SlowMotionComponent()


if __name__ == "__main__":
    init()
    
    video_path = sys.argv[1]
    video_chunk_reader = VideoChunkReader(video_path)
    duration_limit = 40
    last_pos = 0
    all_highlights = {}
    st = SoundComponent.get_name()
    component_confidence_map = {
      SoundComponent.get_name(): 0.9, 
      #SlowMotionComponent.get_name() : 0.9
      }

    while (video_chunk_reader.has_next()):
        chunk = video_chunk_reader.get_next()
        if chunk == None:
          break
        highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
        all_highlights[chunk.get_chunk_position()] = Merger.merge(highlghts_dict, component_confidence_map)
        print(len(all_highlights[chunk.get_chunk_position()]))

    video_chunk_reader.release()
    summarized_highights = Summarizer.summarize(all_highlights, duration_limit)
    
    writer = HighlightsVideoWriter(video_path, "output.mp4", video_chunk_reader.get_video_info(), VideoChunkReader(video_path))
    writer.write(summarized_highights)
    # Output all_highlights
