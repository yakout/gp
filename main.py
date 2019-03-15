# Importing all system components
import crowd
import commentator
import replay
from highlights_processing import Merger, Summarizer

# Initially, game video is on disk

# Define constant of chunk here (something like 5/10 mins depending on the size of the video being loaded)

def get_next_chunk(video_path, last_pos):
  """
    Reads next chunk of video from disk and returns it, updates last_pos
  """
	pass

def init():
  """
  	Initialize all needed structures(map of component confidence), constants, etc...
  """
	pass

if __name__ == "__main__":
  init()
  video_path = from args
  last_pos = 0
  all_highlights = []
  while (!video_read()) {
    chunk, last_pos = get_next_chunk(video_path, last_pos)
    highlghts_dict = component_container.get_chunk_highlights(chunk)
    # get_chunk_highlights calls (crowd, commentator, replay) .get_highlights
    all_highlights.append(Merger.merge(highlights_dict, component_confidence_map))
  }
  
  summarized_highights = Summarizer.summarize(all_highlights, duration_limit)
  # Output all_highlights
