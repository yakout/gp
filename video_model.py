import os

class Chunk():
    """
    This class represents a chunk of the video read from disk.

    Attributes :
        - position : pair denoting the start and end of the chunk w.r.t. video
        - chunk_clip : a VideoFileClip of the clip represented by the chunk
        - shift_frames : frames offset from the start of video.
        - number_of_frames : frames count
    """

    def __init__(self, position, chunk_clip, shift_frames, number_of_frames, start=None, end=None):
        self.position = position
        self.chunk_clip = chunk_clip
        self.shift_frames = shift_frames
        self.number_of_frames = number_of_frames
        self.start = start
        self.end = end

    def __str__(self):
        return "(start: {}, end: {})".format(self.start, self.end)

    __repr__ = __str__

    def get_frame(self, index):
        return self.chunk_clip.get_frame((index - self.shift_frames) / self.chunk_clip.fps)

    def get_frames_count(self):
        return self.number_of_frames

    def get_audio(self):
        audio = self.chunk_clip.audio
        # print("audio extracted from chunk_clip: {}".format(audio.duration))
        return audio

    def get_chunk_position(self):
        return self.position

    def get_clip(self):
        return self.chunk_clip

    def get_fps(self):
        return self.chunk_clip.fps

    def get_chunk_info(self):
        return (self.start, self.end, self.score)



class Highlight():
    """
    This class represents a highlight extracted from the video (represented by
    a range), the start and end indices are relative to the chunk the highlight
    is extracted from.

    Attributes:
        - start_index : start frame of the highlight relative to the chunk
        - end_index : end frame of the highlight relative to the chunk
        - score : score denoting importance of the Highlight between 0 and 1
    """

    def __init__(self, start_index, end_index, score):
        self.start_index = start_index
        self.end_index = end_index
        self.score = score

    def __str__(self):
        return "(start_index: {}, end_index: {}, score: {})".format(self.start_index, self.end_index, self.score)

    __repr__ = __str__

    def set_highlight_endpoints(self, start_index: int, end_index: int):
        self.start_index = start_index
        self.end_index = end_index

    def set_score(self, score: int):
        self.score = score

    def get_score(self):
        return self.score

    def get_highlight_endpoints(self):
        return (self.start_index, self.end_index)
