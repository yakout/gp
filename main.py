# Importing all system components
import sys
from highlights_processing import Merger, Summarizer
from queue import Queue
from component import Chunk, Component, ComponentContainer
import cv2
import numpy as np
from numpy import linalg as LA
import colorama
import time


from SoundComponent import SoundComponent
from video_processing import VideoChunkReader, HighlightsVideoWriter
from general_highlights.replay_detection.SlowMotionComponent import SlowMotionComponent
from highlight_generator import HighlightGenerator

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
    colorama.init() # for windows
    init()
    component_confidence_map = {
        SoundComponent.get_name(): 0.9,
        # SlowMotionComponent.get_name() : 0.9
    }

    # TODO: Add command line input validation checks, add option to use scenes instead of chunk duration(maybe if chunk_duration=0?)
    if (len(sys.argv) < 3):
        print("Invalid number of arguments, usage: <program_name> <video_path> <chunk_duration> [threads num]")
        sys.exit()

    video_path = sys.argv[1]
    chunk_duration = int(sys.argv[2])
    workers_count = 0 # default: No threads, until fixing issues

    if (len(sys.argv) > 3):
        workers_count = int(sys.argv[3])

    # Initialize chunk reader
    video_chunk_reader = VideoChunkReader(
        video_path, chunk_duration=chunk_duration)

    # This is in # of frames atm, should be changed to be in secs/milliseconds
    duration_limit = 1000000
    all_highlights = {}  # Dict of {'chunk_position': List of Highlight}

    if workers_count > 0:
        print(colorama.Fore.BLUE + "Initializing our slaves .." + colorama.Style.RESET_ALL)
        chunks_queue = Queue()
        for i in range(1, workers_count + 1):
            worker = HighlightGenerator(chunks_queue, all_highlights, component_confidence_map, i, video_path)
            worker.daemon = True # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.start()       # Start worker in the background to be ready for consuming chunks once available
            print(colorama.Fore.BLUE + "Worker {} .. done".format(i) + colorama.Style.RESET_ALL)

    highligh_start = time.time()
    # Iterate over all video's chunks and get highlights
    while (video_chunk_reader.has_next()):
        if workers_count > 0:
            chunk = video_chunk_reader.get_next(passive=True)
            if chunk == None:
                break
            print(colorama.Fore.BLUE + "Approximate Queue size: {}".format(chunks_queue.qsize()) + colorama.Style.RESET_ALL)
            chunks_queue.put(chunk)
        else:
            # TODO clean and remove this we don't need it
            chunk = video_chunk_reader.get_next()
            if chunk == None:
                break
            # Get highlights list of each component, highlights_dict = {'component_name': List of Highlight }
            highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
            all_highlights[chunk.get_chunk_position()] = Merger.merge(
                highlghts_dict, component_confidence_map)

    if workers_count > 0:
        print(colorama.Fore.RED + "Waiting until all workers are done .." + colorama.Style.RESET_ALL)
        # Causes the main thread to wait for the queue to finish processing all the chunks
        chunks_queue.join()

    highligh_end = time.time()

    print(colorama.Fore.GREEN + "All workers are done!" + colorama.Style.RESET_ALL)

    summarizer_start = time.time()
    # summarized_highlights = {'chunk_position': List of Highlight} that is more summarized according to user's duration_limit specified
    summarized_highights = Summarizer.summarize(all_highlights, duration_limit)
    summarizer_end = time.time()

    print("Summarized_highights {}".format(summarized_highights))
    writer = HighlightsVideoWriter(video_path,
                                   "output_" +
                                   str(chunk_duration) + "_secs.mp4",
                                   video_chunk_reader.get_video_info(),
                                   VideoChunkReader(video_path, chunk_duration=chunk_duration))

    write_start = time.time()
    writer.write_video(summarized_highights)
    write_end = time.time()
    print("============ STATS ============ ")
    print("Errors count: {} (if the error count is more than 0 please report it to @yakout with the error that appeared in your console".format(ComponentContainer.errors_count))
    print("Video write time(s): {}".format(write_end - write_start))
    print("Summarizer time(s): {}".format(summarizer_end - summarizer_start))
    print("Highlight time(s): {}".format(highligh_end - highligh_start))
