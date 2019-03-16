from video_model.video_model import Chunk 
import cv2
import numpy as np

class VideoChunkReader():

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

    def has_next(self):
        return self.is_reader_opened

    def get_next(self):
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
    def write(highlights):
        pass

if __name__ == "__main__":

    v = VideoChunkReader("videos/bar-mad-sc.mp4")
    chunk = v.get_next()
    print(chunk.get_frames_count())
    # print(chunk.get_frame(9))