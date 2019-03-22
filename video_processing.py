#!/usr/bin/env python3

from video_model import Chunk
import cv2
import numpy as np
from typing import List, Any

import subprocess as sp
import os

from pydub import AudioSegment


class VideoChunkReader():
    """
    This class is responsible for reading chunks of a video file.
    """

    video_path = ""
    chunk_size = 200
    vidcap = None
    is_reader_opened = False
    fps = 0
    audio = []

    def __init__(self, video_path, chunk_size=200):
        self.video_path = video_path
        self.chunk_size = chunk_size
        self.vidcap = cv2.VideoCapture(self.video_path)
        if (self.vidcap.isOpened() == False):
            print("Error opening video stream or file")
        else:
            self.is_reader_opened = True
            self.extract_audio()
            self.fps = self.vidcap.get(cv2.CAP_PROP_FPS)
        self.offset = 0

    def extract_audio(self):
        audio_reader = AudioReader(self.video_path, 'mp3')
        self.audio = audio_reader.get_audio()

    def get_next_audio(self):
        seconds = self.chunk_size / self.fps
        milliseconds = seconds * 1000
        start = self.offset * milliseconds
        end = start + milliseconds
        return self.audio[start: end]

    def has_next(self) -> bool:
        return self.is_reader_opened

    def get_next(self) -> Chunk:
        """
        Returns next available chunk read, or None if no more chunks are available.
        """
        if not self.is_reader_opened:
            return None

        success, image = self.vidcap.read()
        frames_count = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

        captured_frames = []
        count = 0
        while success:
            success, frame = self.vidcap.read()
            if(success):
                count += 1
                captured_frames.append(frame)
                if (count == self.chunk_size):
                    return Chunk(captured_frames)
            else:
                break
        chunk_audio = None
        if (not self.vidcap.isOpened()):
            vidcap.release()
            is_reader_opened = False
        else:
            self.vidcap.SetCaptureProperty(
                cv2.CV_CAP_PROP_POS_FRAMES, offset + len(captured_frames))
            chunk_audio = self.get_next_audio()
            offset = offset + len(captured_frames)
        return Chunk(captured_frames, chunk_audio)


class AudioReader():

    video_path = ""
    audio = []

    def __init__(self, video_path, file_format):
        self.video_path = video_path
        self.issue_ffmpeg_command(file_format, video_path)
        self.extract_audio_file()

    def get_audio(self):
        return self.audio

    def issue_ffmpeg_command(self, file_format, video_path):
        # sp.call(['ffmpeg', '-i', self.video_path, '-f',
        #          file_format, '-ab', '192000', video_path.split('/')[-1].split('.')[0] + ".mp3", 'audio.mp3'])
        sp.call(['ffmpeg', '-i', self.video_path, video_path.split('/')[-1].split('.')[0] + ".mp3"])

    def extract_audio_file(self):
        self.audio = AudioSegment.from_mp3('audio.mp3')


class HighlightsVideoWriter():

    @staticmethod
    def write(highlights_dict):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(config.OUTPUT_PATH +
                                "output.mp4", fourcc, fps, (width, height))
        for chunk, highlights in highlights_dict.items():
            for highlight in highlights:
                start, end = highlight.get_highlight_endpoints()
                for frame_index in range(start, end + 1):
                    video.write(chunk.get_frame(frame_index))
        video.release()


# if __name__ == "__main__":
#     reader = AudioReader("videos/bar-mad-sc.mp4", "mp3")
#     audio = reader.get_audio()
#     print(len(audio))

#     vid_chunk = VideoChunkReader("videos/bar-mad-sc.mp4")
#     # chunk = v.get_next()
#     # print(chunk.get_frames_count())
#     counter = 0
#     while (vid_chunk.has_next()):
#         chunk = vid_chunk.get_next()
#         print("Chunk " + str(counter))
#         counter += 1
#         for i in range(chunk.get_frames_count()):
#             frame = chunk.get_frame(i)
#             print(frame.shape)
#             cv2.imshow('Frame',frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#     # print(chunk.get_frame(9))
#     pass
