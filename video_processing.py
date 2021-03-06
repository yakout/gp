import os
import moviepy.editor as mpe

from typing import List, Any
from moviepy.editor import concatenate_videoclips
from video_model import Chunk
from scenedetector import find_scenes

class VideoChunkReader():
    """
    This class is responsible for reading chunks of a video file.

    chunk_duration: if 0 we use shot detection (scenes)
    """

    def __init__(self, video_path, chunk_duration=120):
        self.video_clip = mpe.VideoFileClip(video_path, verbose=False)
        self.number_of_frames = int(
            self.video_clip.fps * self.video_clip.duration)
        self.fps = self.video_clip.fps
        self.chunk_idx = 0
        self.video_dimensions = self.video_clip.size
        self.offset = 0
        self.last_time_read = 0
        self.chunk_duration = chunk_duration
        self.scenes = find_scenes(
            video_path) if self.chunk_duration == 0 else []

    def get_fps(self):
        return self.fps

    def get_video_info(self):
        return {
            'fps': self.fps,
            'dimensions': self.video_dimensions
        }

    def has_next(self) -> bool:
        return self.chunk_idx < len(self.scenes) if self.chunk_duration == 0 else self.last_time_read < self.video_clip.duration

    def get_next(self, passive=False) -> Chunk:
        """
        Returns next available chunk read, or None if no more chunks are available.
        """

        # Check if scenes are used or a fixed duration
        # if duration is 0 we use shot detection otherwise we read using moviepy
        if (self.chunk_duration != 0):
            start = self.last_time_read
            end = min(self.last_time_read + self.chunk_duration, self.video_clip.duration)
            if passive:
                chunk_clip = None
                self.last_time_read += (end - start)
            else:
                chunk_clip = self.video_clip.subclip(start, end)
                self.last_time_read += chunk_clip.duration
        else:
            # Shot detection
            start = int(self.scenes[self.chunk_idx][0].get_frames() / self.fps)
            end = int(self.scenes[self.chunk_idx][1].get_frames() / self.fps)
            if passive: # Don't read the clip, just return it's endpoints
                chunk_clip = None
            else:
                chunk_clip = self.video_clip.subclip(start, end)

        # print("Chunk Duration! {}".format(chunk_clip.duration))
        # number_of_frames = int(chunk_clip.fps * chunk_clip.duration)
        number_of_frames = int(self.fps * (end - start))

        position = (self.offset, self.offset + number_of_frames)
        # print("chunk position {}, captured_frames size {}".format(position, number_of_frames))
        self.offset += number_of_frames
        self.chunk_idx += 1
        return Chunk(position, chunk_clip, self.offset - number_of_frames, number_of_frames, start, end) # TODO cleanup the start and end args

    def reset(self):
        self.chunk_idx = 0
        self.offset = 0
        self.last_time_read = 0


class HighlightsVideoWriter():
    """
    This class is responsible for writing the video after generating the
    highlight, it should take the same reader using for reading the video,
    """
    def __init__(self, output_path, video_chunk_reader):
        self.output_path = output_path
        self.video_chunk_reader = video_chunk_reader
        self.video_chunk_reader.reset() # reset reader values

    def write_video(self, highlights_dict):
        # Object to concatenate all highlight clips in
        total_video_clip = None

        # FPS to read video with
        fps = self.video_chunk_reader.get_fps()
        # print("Video Frames per second = {}".format(fps))

        # Total frames already read
        total_frames_passed = 0
        while (self.video_chunk_reader.has_next()):
            # print("total_frames_passed: {}".format(total_frames_passed))
            # Get next chunk
            chunk = self.video_chunk_reader.get_next()
            if chunk == None:
                break
            chunk_clip = chunk.get_clip()
            if (chunk_clip is None):
                # print("Chunk clip is None")
                continue

            # If chunk doesn't have any highlights continue
            if chunk.get_chunk_position() not in highlights_dict:
                # print("chunk has no highlight. chunk pos: {}".format(chunk.get_chunk_position()))
                total_frames_passed += fps * chunk_clip.duration
                continue

            # Else, get chunk highlights
            highlights = highlights_dict[chunk.get_chunk_position()]
            for highlight in highlights:
                # For each highlight get starting/ending frames of video
                start_frame, end_frame = highlight.get_highlight_endpoints()
                # print("Chunk Boundaries in frames (absolute) : ",
                #       str(start_frame), str(end_frame))

                # Subtracting total frames passed to make start_frame, end_frame relative to current chunk
                start_frame -= total_frames_passed
                end_frame -= total_frames_passed

                # Get clip corresponding to highlight
                cut_clip = chunk_clip.subclip(
                    start_frame / fps, end_frame / fps)

                # print("cut_clip duration = {}".format(cut_clip.duration))

                # Concatenate to total video
                if total_video_clip is None:
                    total_video_clip = cut_clip
                else:
                    # print("total_video__clip duration = {}".format(
                    #     total_video_clip.duration))
                    total_video_clip = concatenate_videoclips(
                        [total_video_clip, cut_clip])
            # Update total frames passsed
            total_frames_passed += fps * chunk_clip.duration
        # Write concatenated highlights clips to file
        if total_video_clip is not None:
            total_video_clip.write_videofile(self.output_path)
        else:
            print("No highlights written")
