import sys
import numpy as np
import colorama
import time
import os
import datetime

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

# WebSocket Server imports
from flask import Flask
from flask_socketio import SocketIO, emit

# config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


# Deactivating tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def init():
    """
    Initialize all needed structures(map of component confidence), constants, etc...
    """
    # {: 0.9, 'video': 0.5, }
    # registering components
    SoundComponent()
    # ReplayDetectionComponent()
    # SlowMotionComponent()



@app.route('/')
def serve_static_index():
    return 'Hello world'

@socketio.on('generate_highlights')
def generate(json):
    video_path     = json['video_path']
    chunk_duration = json['chunk_duration']
    duration_limit = json['duration_limit']

    # Initialize chunk reader
    video_chunk_reader = VideoChunkReader(video_path, chunk_duration=chunk_duration)

    all_highlights = {}  # Dict of {'chunk_position': List of Highlight}
    chunks_length_dict = {} # Dict of {'chunk_position' : length in frames}

    # Iterate over all video's chunks and get highlights
    while (video_chunk_reader.has_next()):
        chunk = video_chunk_reader.get_next()
        if chunk == None:
            break
        # Get highlights list of each component, highlights_dict = {'component_name': List of Highlight }
        highlghts_dict = ComponentContainer.get_chunk_highlights(chunk)
        all_highlights[chunk.get_chunk_position()] = Merger.merge(
            highlghts_dict, component_confidence_map)
        for highlight in all_highlights[chunk.get_chunk_position()]:
            endpoints = highlight.get_highlight_endpoints()
            endpoints_sec = [x / video_chunk_reader.get_fps() for x in endpoints]
            start_time = str(datetime.timedelta(seconds=endpoints_sec[0]))
            end_time = str(datetime.timedelta(seconds=endpoints_sec[1]))
            emit('receive_highlights', [start_time, end_time, highlight.get_score()])
        chunks_length_dict[chunk.get_chunk_position()
                            ] = chunk.get_frames_count()

    # summarized_highlights = {'chunk_position': List of Highlight} that is more summarized according to user's duration_limit specified
    summarized_highights = Summarizer.summarize(all_highlights, duration_limit, video_chunk_reader.fps)


    print("Summarized_highights {}".format(summarized_highights))

    output_path = "client/public/output/"
    video_output_path = output_path + "output_" + str(chunk_duration) + "_secs.mp4"
    writer = HighlightsVideoWriter(video_output_path, video_chunk_reader)
    writer.write_video(summarized_highights)
    emit('receive_highlight_reel', video_output_path)


if __name__ == "__main__":
    init()
    component_confidence_map = {
        SoundComponent.get_name(): 0.9,
        # ReplayDetectionComponent.get_name(): 0.9
        # SlowMotionComponent.get_name() : 0.9
    }

    # init server
    print("Running WebSocket server ..")
    socketio.run(app)
