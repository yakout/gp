import colorama
import time
import traceback

import moviepy.editor as mpe

from queue import Queue
from threading import Thread

from component import Chunk, Component, ComponentContainer
from highlights_processing import Merger

# WebSocket Server imports
from flask import Flask
from flask_socketio import SocketIO, emit

class HighlightGenerator(Thread):
  """
  Note the retry mechanism is only to ensure reliability of workers jst in case
  unexpected errors that is related to race conditions happened (hopefully not).
  """
  def __init__(self, queue, all_highlights_dict, component_confidence_map, worker_num, video_path):
    Thread.__init__(self)
    self.queue = queue
    self.all_highlights_dict = all_highlights_dict
    self.component_confidence_map = component_confidence_map
    self.worker_num = worker_num
    self.retry_count = 3
    self.wait_time = 0 # in seconds
    self.video_clip = mpe.VideoFileClip(video_path, verbose=False)

  def run(self):
    while True:
      chunk = self.queue.get()
      chunk_clip = self.video_clip.subclip(chunk.start, chunk.end)
      chunk.chunk_clip = chunk_clip
      try:
        if chunk is None or chunk.chunk_clip is None:
          continue
        print(colorama.Fore.GREEN + "Worker {}: processing new job. chunk: {}".format(self.worker_num, chunk) + colorama.Style.RESET_ALL)
        # Get highlights list of each component, highlights_dict = {'component_name': List of Highlight}
        highlghts_dict = {}
        done = False
        while(not done):
          if self.wait_time > 0:
            time.sleep(self.wait_time)
          try:
            highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
            done = True
            self.wait_time = 0
            print(colorama.Fore.GREEN + "Worker {}: processing new job done.".format(self.worker_num) + colorama.Style.RESET_ALL)
          except Exception as _:
            print(colorama.Fore.GREEN + "Worker {}: recovered from error. stacktrace:\n{}".format(self.worker_num, traceback.format_exc()) + colorama.Style.RESET_ALL)
            ComponentContainer.errors_count += 1
            self.retry_count -= 1
            self.wait_time = 1 + self.wait_time * 2
            if self.retry_count == 0:
              print(colorama.Fore.GREEN + "Worker {}: Retries exausted!".format(self.worker_num) + colorama.Style.RESET_ALL)
              self.wait_time = 0
              self.retry_count = 10
              break


        print(colorama.Fore.GREEN + "Worker {}: highlights found {}".format(self.worker_num, highlghts_dict) + colorama.Style.RESET_ALL)
        self.all_highlights_dict[chunk.get_chunk_position()] = Merger.merge(highlghts_dict, self.component_confidence_map)
        emit(chunk.get_chunk_position())
      finally:
        self.queue.task_done()
