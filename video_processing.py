#!/usr/bin/env python3

from video_model import Chunk
import cv2
import numpy as np
from typing import List, Any

import subprocess as sp
import os

from pydub import AudioSegment

import moviepy.editor as mpe
from moviepy.editor import concatenate_videoclips
from general_highlights.replay_detection.SlowMotionComponent import SlowMotionComponent

from scenedetector import *


class VideoChunkReader():
    """
    This class is responsible for reading chunks of a video file.
    """

    def __init__(self, video_path, chunk_duration=120):
        self.video_clip = mpe.VideoFileClip(video_path)
        self.number_of_frames = int(
            self.video_clip.fps * self.video_clip.duration)
        self.fps = self.video_clip.fps
        self.chunk_idx = 0
        self.video_dimensions = self.video_clip.size
        self.offset = 0
        self.last_time_read = 0
        self.chunk_duration = chunk_duration
        # self.scenes = find_scenes(video_path)

    def get_fps(self):
        return self.fps

    def get_video_info(self):
        return {
            'fps': self.fps,
            'dimensions': self.video_dimensions
        }

    def has_next(self) -> bool:
        return self.last_time_read < self.video_clip.duration
        # return self.chunk_idx < len(self.scenes)

    def get_next(self) -> Chunk:
        """
        Returns next available chunk read, or None if no more chunks are available.
        """

        # shot detection
        # start = self.scenes[self.chunk_idx][0].get_timecode()
        # end = self.scenes[self.chunk_idx][1].get_timecode()
        # chunk_clip = self.video_clip.subclip(start, end)

        chunk_clip = self.video_clip.subclip(
            self.last_time_read, min(self.last_time_read + self.chunk_duration, self.video_clip.duration))
        self.last_time_read += self.chunk_duration
        number_of_frames = int(chunk_clip.fps * chunk_clip.duration)

        position = (self.offset, self.offset + number_of_frames)
        # print("chunk position {}, captured_frames size {}".format(position, number_of_frames))
        self.offset += number_of_frames
        self.chunk_idx += 1
        return Chunk(position, chunk_clip, self.offset - number_of_frames, number_of_frames)


class HighlightsVideoWriter():

    def __init__(self, video_path, output_path, video_info, video_chunk_reader):
        self.video_path = video_path
        self.output_path = output_path
        self.video_info = video_info
        self.video_chunk_reader = video_chunk_reader

    def write_video(self, highlights_dict):
        # Object to concatenate all highlight clips in
        total_video_clip = None

        # FPS to read video with
        fps = self.video_chunk_reader.get_fps()
        print("Video Frames per second = {}".format(fps))

        # Total frames already read
        total_frames_passed = 0
        while (self.video_chunk_reader.has_next()):
            # Get next chunk
            chunk = self.video_chunk_reader.get_next()
            if chunk == None:
                break
            chunk_clip = chunk.get_clip()

            # If chunk doesn't have any highlights continue
            if chunk.get_chunk_position() not in highlights_dict:
                total_frames_passed += fps * chunk_clip.duration
                continue

            # Else, get chunk highlights
            highlights = highlights_dict[chunk.get_chunk_position()]
            for highlight in highlights:
                # For each highlight get starting/ending frames of video
                start_frame, end_frame = highlight.get_highlight_endpoints()
                print("Chunk Boundaries in frames (absolute) : ",
                      str(start_frame), str(end_frame))

                # Subtracting total frames passed to make start_frame, end_frame relative to current chunk
                start_frame -= total_frames_passed
                end_frame -= total_frames_passed

                # Get clip corresponding to highlight
                cut_clip = chunk_clip.subclip(
                    start_frame / fps, end_frame / fps)

                # Concatenate to total video
                if total_video_clip is None:
                    total_video_clip = cut_clip
                else:
                    total_video_clip = concatenate_videoclips(
                        [total_video_clip, cut_clip])
            # Update total frames passsed
            total_frames_passed += fps * chunk_clip.duration
        # Write concatenated highlights clips to file
        total_video_clip.write_videofile(self.output_path)
