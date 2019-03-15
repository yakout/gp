class Chunk():

	def __init__(self):
		self.frames = []

	def set_frames(self, frames):
		self.frames = frames

	def get_frame(self, index):
		return frames[index]

	def get_frames_count(self):
		return len(frames)

class Highlight():

	def __init__(self):
		self.start_index = 0
		self.end_index = 0
		self.score = 0

	def set_highlight_endpoints(self, start_index, end_index):
		self.start_index = start_index
		self.end_index = end_index

	def set_score(self, score):
		self.score = score

	def get_score(self):
		return self.score

	def get_highlight_endpoints(self):
		return (self.start_index, self.end_index)