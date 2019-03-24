class Chunk():
    """
    This class represents a chunk of the video read from disk.
    """
    def __init__(self, frames=None, audio=None, position):
        self.frames = frames
        self.audio = audio
        self.position = position

    def set_frames(self, frames):
        self.frames = frames

    def get_frame(self, index):
        return self.frames[index]

    def get_frames(self):
        return self.frames

    def get_frames_count(self):
        return len(self.frames)

    def get_audio(self):
        return self.audio

    def get_chunk_position(self):
        return self.position


class Highlight():
    """
This class represents a highlight extracted from the video (represented by
    a range), the start and end indices are relative to the chunk the highlight
    is extracted from.
"""

    def __init__(self, start_index, end_index, score):
        self.start_index = start_index
        self.end_index = end_index
        self.score = score

    def set_highlight_endpoints(self, start_index: int, end_index: int):
        self.start_index = start_index
        self.end_index = end_index

    def set_score(self, score: int):
        self.score = score

    def get_score(self):
        return self.score

    def get_highlight_endpoints(self):
        return (self.start_index, self.end_index)