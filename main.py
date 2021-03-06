import sys
import numpy as np
import colorama
import time
import os

from queue import Queue
from numpy import linalg as LA

# Importing all system components
from highlights_processing import Merger, Summarizer
from component import Chunk, Component, ComponentContainer
from SoundComponent import SoundComponent
from video_processing import VideoChunkReader, HighlightsVideoWriter
from general_highlights.replay_detection.SlowMotionComponent import SlowMotionComponent
from general_highlights.replay_detection.ReplayDetectionComponent import ReplayDetectionComponent

from highlight_generator import HighlightGenerator

from system_evaluator import SystemEvaluator

# Deactivating tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def init():
    """
    Initialize all needed structures(map of component confidence), constants, etc...
    """
    # {: 0.9, 'video': 0.5, }

    # registering components
    SoundComponent()
    ReplayDetectionComponent()
    # SlowMotionComponent()


if __name__ == "__main__":
    total_time_start = time.time()

    # init colorama for windows
    colorama.init()

    # Initialize Components and Components' confidence map
    init()
    component_confidence_map = {
        SoundComponent.get_name(): 1,
        ReplayDetectionComponent.get_name(): 1
    }

    # TODO: Add command line input validation checks, add option to use scenes instead of chunk duration(maybe if chunk_duration=0?)
    if (len(sys.argv) < 3):
        print(
            "Invalid number of arguments, usage: <program_name> <video_path> <chunk_duration> [workers num] [video output limit in minutes]")
        sys.exit()

    video_path = sys.argv[1]
    chunk_duration = int(sys.argv[2])  # in seconds
    workers_count = 0  # Default: No threads
    duration_limit = 10  # Default: 10 mins

    if (len(sys.argv) > 3):
        workers_count = int(sys.argv[3])

    if (len(sys.argv) > 4):
        duration_limit = int(sys.argv[4])

    # Initialize chunk reader
    video_chunk_reader = VideoChunkReader(video_path,
                                          chunk_duration=chunk_duration)

    all_highlights = {}  # Dict of {'chunk_position': List of Highlight}
    chunks_length_dict = {}  # Dict of {'chunk_position' : length in frames}

    if workers_count > 0:
        print(colorama.Fore.YELLOW + "Initializing our slaves .." +
              colorama.Style.RESET_ALL)
        chunks_queue = Queue()
        for i in range(1, workers_count + 1):
            worker = HighlightGenerator(
                chunks_queue, all_highlights, chunks_length_dict, component_confidence_map, i, video_path)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            worker.daemon = True
            # Start worker in the background to be ready for consuming chunks once available
            worker.start()
            print(colorama.Fore.BLUE + "Worker {} .. done".format(i) +
                  colorama.Style.RESET_ALL)

    highlight_start = time.time()
    # Iterate over all video's chunks and get highlights
    while (video_chunk_reader.has_next()):
        if workers_count > 0:
            chunk = video_chunk_reader.get_next(passive=True)
            if chunk == None:
                break
            print(colorama.Fore.BLUE + "Approximate Queue size: {}".format(
                chunks_queue.qsize()) + colorama.Style.RESET_ALL)
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
            chunks_length_dict[chunk.get_chunk_position()
                               ] = chunk.get_frames_count()

    if workers_count > 0:
        print(colorama.Fore.RED + "Waiting until all workers are done .." +
              colorama.Style.RESET_ALL)
        # Causes the main thread to wait for the queue to finish processing all the chunks
        chunks_queue.join()

    highlight_end = time.time()

    print(colorama.Fore.GREEN + "All workers are done!" + colorama.Style.RESET_ALL)

    summarizer_start = time.time()
    # summarized_highlights = {'chunk_position': List of Highlight} that is more summarized according to user's duration_limit specified
    summarized_highights = Summarizer.summarize(
        all_highlights, duration_limit, video_chunk_reader.fps)
    summarizer_end = time.time()

    print("Summarized_highights {}".format(summarized_highights))

    write_start = time.time()
    writer = HighlightsVideoWriter("output_" + str(chunk_duration) + "_secs.mp4",
                                   video_chunk_reader)
    writer.write_video(summarized_highights)
    write_end = time.time()

    total_time_end = time.time()
    # Evaluation
    print("============ EVALUATION ============ ")
    evaluator = SystemEvaluator(video_path)
    accurracy, precision, recall, f1  = evaluator.evaluate(summarized_highights, chunks_length_dict)
    print("Evaluation results : accuracy = {}\n precision = {}\n recall = {}\n f1 = {}\n"
            .format(accurracy, precision, recall, f1))

    # benchmarking
    print("============ STATS ============ ")
    print("Errors count: {}".format(ComponentContainer.errors_count) + colorama.Fore.RED +
          "\n(NOTE! If the error count is more than 0 please report it to @yakout with the error that appeared in your console!)" + colorama.Style.RESET_ALL)
    print("Video write time: {} mins".format((write_end - write_start) / 60))
    print("Summarizer time: {} seconds".format(
        summarizer_end - summarizer_start))
    print("Highlight generation time: {} mins".format(
        (highlight_end - highlight_start) / 60))
    print("Total time: {} mins".format(
        (total_time_end - total_time_start) / 60))
    print("=============================== ")
