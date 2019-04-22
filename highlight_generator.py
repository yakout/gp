from queue import Queue
from threading import Thread
from component import Chunk, Component, ComponentContainer
from highlights_processing import Merger
import colorama

class HighlightGenerator(Thread):
  def __init__(self, queue, all_highlights_dict, component_confidence_map, worker_num):
    Thread.__init__(self)
    self.queue = queue
    self.all_highlights_dict = all_highlights_dict
    self.component_confidence_map = component_confidence_map
    self.worker_num = worker_num

  def run(self):
    while True:
      chunk = self.queue.get()
      try:
        if chunk is None or chunk.chunk_clip is None:
          continue
        print(colorama.Fore.GREEN + "Worker {}: processing new job. chunk: {}".format(self.worker_num, chunk.chunk_clip) + colorama.Style.RESET_ALL)
        # Get highlights list of each component, highlights_dict = {'component_name': List of Highlight}
        highlghts_dict = {}
        try:
         highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
        except IndexError as e:
          print(colorama.Fore.GREEN + "Worker {}: error occurred {}".format(self.worker_num, e) + colorama.Style.RESET_ALL)

        print(colorama.Fore.GREEN + "Worker {}: highlights found {}".format(self.worker_num, highlghts_dict) + colorama.Style.RESET_ALL)
        self.all_highlights_dict[chunk.get_chunk_position()] = Merger.merge(highlghts_dict, self.component_confidence_map)
      finally:
        self.queue.task_done()
