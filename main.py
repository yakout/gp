# Importing all system components
import sys
from highlights_processing import Merger, Summarizer
from component.component import Chunk, Component
import cv2
import numpy as np
import config
from numpy import linalg as LA
from general_highlights.replay_detection import ZeroCrossing as zc
from utils.video_processing import VideoChunkReader


# Initially, game video is on disk

# Define constant of chunk here (something like 5/10 mins depending on the size of the video being loaded)

def init():
    """
      Initialize all needed structures(map of component confidence), constants, etc...
    """
    # {: 0.9, 'video': 0.5, }

if __name__ == "__main__":
  init()
  video_path = sys.argv[0]
  video_chunk_reader = VideoChunkReader(video_path)
  last_pos = 0
  all_highlights = {}
  while (video_chunk_reader.has_next()):
    # chunk, last_pos = get_next_chunk(video_path, last_pos)
    chunk = video_chunk_reader.get_next_chunk()
    highlghts_dict = component_container.get_chunk_highlights(chunk)
    # get_chunk_highlights calls (crowd, commentator, replay) .get_highlights
    # all_highlights.append(Merger.merge(highlights_dict, component_confidence_map))
    all_highlights[chunk] = Merger.merge(highlights_dict, component_confidence_map)

  summarized_highights = Summarizer.summarize(all_highlights, duration_limit)

  # Output all_highlights
