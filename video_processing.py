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
        self.vidcap = cv2.VideoCapture(self.video_path)
        self.video_clip = mpe.VideoFileClip(self.video_path)
        self.fps = 0
        self.chunk_idx = 0
        self.shift_frames = 0

        if (self.vidcap.isOpened() == False):
            print("Error opening video stream or file.")
        else:
            print("Extracting audio...")
            self.is_reader_opened = True
            self.extract_audio()
            print("Audio of length " + str(len(self.audio)) + " was extracted.")
            self.fps = self.vidcap.get(cv2.CAP_PROP_FPS)
            self.video_dimensions = (int(self.vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                     int(self.vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.offset = 0
        self.audio_offset = 0

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
        return self.is_reader_opened

    def get_next(self) -> Chunk:
        """
        Returns next available chunk read, or None if no more chunks are available.
        """
        if not self.is_reader_opened:
            return None

        success, _ = self.vidcap.read()
        # frames_count = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)


        # captured_frames = []
        # count = 0
        # while success:
        #     success, frame = self.vidcap.read()
        #     if(success):
        #         count += 1
        #         captured_frames.append(frame)
        #         if (count == self.chunk_size):
        #             break
        #     else:
        #         break

        # shot detection
        start_index = self.shift_frames
        end_index = self.shift_frames + self.chunk_size - 1

        chunk_clip = self.video_clip.cutout(start_index/self.fps, end_index/self.fps)
        number_of_frames = int(chunk_clip.fps * chunk_clip.duration)

        chunk_audio = None
        position = None
        if (not self.vidcap.isOpened() or not success):
            self.vidcap.release()
            self.is_reader_opened = False
            return None
        else:
            self.vidcap.set(cv2.CAP_PROP_POS_FRAMES,
                            self.offset + number_of_frames)
            # self.vidcap.SetCaptureProperty(
            #     cv2.CV_CAP_PROP_POS_FRAMES, offset + len(captured_frames))
            chunk_audio = self.get_next_audio()
            position = (self.offset, self.offset + number_of_frames)
            self.offset = self.offset + number_of_frames
        print("chunk position {}, captured_frames size {}".format(position, number_of_frames))

        return Chunk(position, chunk_clip, self.offset-number_of_frames, number_of_frames, chunk_audio)

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
        for frame in chunk.get_clip().iter_frames():
            # print(frame.shape)
            cv2.imshow('Frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # print(chunk.get_frame(9))
    pass
