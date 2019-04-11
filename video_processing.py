#!/usr/bin/env python3

from video_model import Chunk
import cv2
import numpy as np
from typing import List, Any

import subprocess as sp
import os

from pydub import AudioSegment

import moviepy.editor as mpe
from general_highlights.replay_detection.SlowMotionComponent import SlowMotionComponent

from scenedetector import *

class VideoChunkReader():
    """
    This class is responsible for reading chunks of a video file.
    """

    def __init__(self, video_path, chunk_size=1000):
        self.audio = []
        self.is_reader_opened = False
        self.video_dimensions = (0, 0)
        self.video_path = video_path
        self.chunk_size = chunk_size
        self.video_clip = mpe.VideoFileClip(self.video_path)
        self.number_of_frames = int(self.video_clip.fps * self.video_clip.duration)
        self.fps = 0
        self.chunk_idx = 0
        self.fps = self.video_clip.fps
        self.video_dimensions = self.video_clip.size
        self.offset = 0
        self.audio_offset = 0
        self.scenes = find_scenes(video_path)
        print("scenes", self.scenes)

    def extract_audio(self):
        audio_reader = AudioReader(self.video_path, 'mp3')
        self.audio = audio_reader.get_audio()
        print("Extracted audio {}".format(self.audio))

    def get_next_audio(self):
        seconds = self.chunk_size / self.fps
        milliseconds = seconds * 1000
        start = self.audio_offset
        end = start + milliseconds
        self.audio_offset = end
        print("\t========")
        print("start, end = {}, {}".format(start, end))
        print("len(self.audio) = {}".format(len(self.audio)))
        print("\t========")
        return self.audio[start: end]

    def get_fps(self):
        return self.fps

    def get_video_info(self):
        return {
            'fps': self.fps,
            'dimensions': self.video_dimensions
        }

    def has_next(self) -> bool:
        return self.chunk_idx < len(self.scenes)

    def get_next(self) -> Chunk:
        """
        Returns next available chunk read, or None if no more chunks are available.
        """

        # shot detection

        start = self.scenes[self.chunk_idx][0].get_timecode()
        end = self.scenes[self.chunk_idx][1].get_timecode()

        chunk_clip = self.video_clip.subclip(start, end)
        number_of_frames = int(chunk_clip.fps * chunk_clip.duration)

        position = (self.offset, self.offset + number_of_frames)
        print("chunk position {}, captured_frames size {}".format(position, number_of_frames))
        self.offset = self.offset + number_of_frames

        self.chunk_idx += 1
        return Chunk(position, chunk_clip, self.offset-number_of_frames, number_of_frames)

    def release(self):
        self.vidcap.release()


class AudioReader():
    def __init__(self, video_path, file_format):
        self.audio = []
        self.video_path = video_path
        self.audio_path = self.video_path.split('/')[-1].split('.')[0] + ".mp3"
        self.issue_ffmpeg_command(file_format)
        self.extract_audio_file()

    def get_audio(self):
        return self.audio

    def issue_ffmpeg_command(self, file_format):
        # sp.call(['ffmpeg', '-i', self.video_path, '-f',
        #          file_format, '-ab', '192000', video_path.split('/')[-1].split('.')[0] + ".mp3", 'audio.mp3'])
        sp.call(['ffmpeg', '-i', self.video_path, '-ar', '44100', self.audio_path])

    def extract_audio_file(self):
        self.audio = AudioSegment.from_file(self.audio_path, frame_rate=22050, sample_width=2)


class HighlightsVideoWriter():

    def __init__(self, video_path, output_path, video_info, video_chunk_reader):
        self.video_path = video_path
        self.output_path = output_path
        self.video_info = video_info
        self.video_chunk_reader = video_chunk_reader

    def write(self, highlights_dict):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(self.output_path,
                                fourcc,
                                self.video_chunk_reader.get_fps(),
                                self.video_info['dimensions'])

        while (self.video_chunk_reader.has_next()):
            chunk = self.video_chunk_reader.get_next()
            if chunk == None:
                break
            if chunk.get_chunk_position() not in highlights_dict:
                continue
            highlights = highlights_dict[chunk.get_chunk_position()]
            for highlight in highlights:
                start, end = highlight.get_highlight_endpoints()
                for frame_index in range(start, end + 1):
                    print("#write frame_index {}".format(frame_index))
                    video.write(chunk.get_frame(frame_index % self.video_chunk_reader.chunk_size))
        video.release()


if __name__ == "__main__":
    # reader = AudioReader("videos/bar-mad-sc.mp4", "mp3")
    # audio = reader.get_audio()
    # print(len(audio))

    vid_chunk = VideoChunkReader("videos/Liverpool vs Porto 2 0 Goals and Highlights 2019 HD.mp4")

    # chunk = v.get_next()
    # print(chunk.get_frames_count())
    counter = 0
    slow_motion = SlowMotionComponent()

    while (vid_chunk.has_next()):
        chunk = vid_chunk.get_next()

        print("Chunk " + str(counter))
        slow_motion.get_highlights(chunk)
        counter += 1
        chunk.get_clip().audio.write_audiofile("first.mp3")
        print(chunk.get_audio())

        for frame in chunk.get_clip().iter_frames():
            # print(frame.shape)
            cv2.imshow('Frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # print(chunk.get_frame(9))
    pass
