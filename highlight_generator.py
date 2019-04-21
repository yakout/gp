from queue import Queue
from threading import Thread
from component import Chunk, Component, ComponentContainer
from highlights_processing import Merger

class HighlightGenerator(Thread):
  def __init__(self, queue, all_highlights_dict, component_confidence_map):
    Thread.__init__(self)
    self.queue = queue
    self.all_highlights_dict = all_highlights_dict
    self.component_confidence_map = component_confidence_map

  def run(self):
    while True:
      chunk = self.queue.get()
      try:
        # Get highlights list of each component, highlights_dict = {'component_name': List of Highlight}
        highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
        self.all_highlights_dict[chunk.get_chunk_position()] = Merger.merge(highlghts_dict, self.component_confidence_map)
      finally:
        self.queue.task_done()
