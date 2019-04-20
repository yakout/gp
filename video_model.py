from pydub import AudioSegment
import os


class Chunk():
    """
    This class represents a chunk of the video read from disk.
    """

    def __init__(self, position, chunk_clip, shift_frames, number_of_frames):
        self.position = position
        self.chunk_clip = chunk_clip
        self.shift_frames = shift_frames
        self.number_of_frames = number_of_frames

    def get_frame(self, index):
        return self.chunk_clip.get_frame((index - self.shift_frames) / self.chunk_clip.fps)

    def get_frames_count(self):
        return self.number_of_frames

    def get_audio(self):
        audio = self.chunk_clip.audio
        file_path = "clip_audio_" + str(self.position[0]) + ".mp3"
        # print("Writing new audio file for chunk #{}".format(self.position[0]))
        audio.write_audiofile(file_path)

        # pydub returns array of audio in milliseconds
        audio = AudioSegment.from_mp3(file_path)

        # Remove mp3 file created, uncomment to monitor all mp3 files created for each chunk
        os.remove(file_path)
        return audio

    def get_chunk_position(self):
        return self.position

    def get_clip(self):
        return self.chunk_clip


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
