from video_model.video_model import Chunk
import cv2
import numpy as np
from typing import List, Any

class VideoChunkReader():
    """
    This class is responsible for reading chunks of a video file.
    """

    video_path = ""
    chunk_size = 200
    vidcap = None
    is_reader_opened = False
    offset = 0

    def __init__(self, video_path, chunk_size=200):
        self.video_path = video_path
        self.chunk_size = chunk_size
        self.vidcap = cv2.VideoCapture(self.video_path)
        if (self.vidcap.isOpened() == False):
            print("Error opening video stream or file")
        else:
            self.is_reader_opened = True

    def has_next(self) -> bool:
        return self.is_reader_opened

    def get_next(self) -> Chunk:
        """
        Returns next available chunk read, or None if no more chunks are available.
        """
        if not self.is_reader_opened:
            return None

        success,image = self.vidcap.read()
        frames_count = self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

        captured_frames = []
        count = 0
        while success:
            success,frame = self.vidcap.read()
            if(success):
                count += 1
                captured_frames.append(frame)
                if (count == self.chunk_size):
                    return Chunk(captured_frames)
            else:
                break

        if (not self.vidcap.isOpened()):
            vidcap.release()
            is_reader_opened = False
        else:
            self.vidcap.SetCaptureProperty(cv2.CV_CAP_PROP_POS_FRAMES, offset + len(captured_frames))
            offset = offset + len(captured_frames)
        return Chunk(captured_frames)


class HighlightsVideoWriter():

    @staticmethod
    def write(highlights_dict):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(config.OUTPUT_PATH + "output.mp4", fourcc, fps, (width,height))
        for chunk, highlights in highlights_dict.items():
            for highlight in highlights:
                start ,end =  highlight.get_highlight_endpoints()
                for frame_index in range(start, end + 1):
                    video.write(chunk.get_frame(frame_index))
        video.release()


if __name__ == "__main__":

    vid_chunk = VideoChunkReader("videos/bar-mad-sc.mp4")
    # chunk = v.get_next()
    # print(chunk.get_frames_count())
    counter = 0
    while (vid_chunk.has_next()):
        chunk = vid_chunk.get_next()
        print("Chunk " + str(counter))
        counter += 1
        for i in range(chunk.get_frames_count()):
            frame = chunk.get_frame(i)
            print(frame.shape)
            cv2.imshow('Frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    # print(chunk.get_frame(9))
