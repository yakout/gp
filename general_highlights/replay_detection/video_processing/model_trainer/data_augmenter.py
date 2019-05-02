from moviepy.editor import *

class DataAugmenter():
    sizes = [(1280,720), (720,480), (480, 240), (360,180), (240, 120)]


    def getDifferentSize(self, chunk):
        augmented_chunks = []
        for size in self.sizes:
            augmented_chunks.appen(chunk.copy().resize(size))

        return augmented_chunks
