from abc import ABC, abstractmethod
import sys
import shutil
import os
from classifier import AudioClassifier
from video_model import Highlight, Chunk
from component import Component, ComponentContainer

class SoundComponent(Component):

    def __init__(self):
        self.write_path = "data/"
        self.window_size = 6000 # 6 sec window

        ComponentContainer.register_component(SoundComponent.get_name(), self)

    @staticmethod
    def get_name():
        return 'sound'

    @abstractmethod
    def get_highlights(self, chunk: Chunk) -> 'List[Highlight]':
        """
        Gets highlights for this video chunk as per this component's perspective.
        :param chunk: the current video chunk being processed
        :return: list of highlights from given chunk
        """
        audio = chunk.get_audio()

        self.generate_mp3(audio)

        self.generate_data_txt(len(audio) // self.window_size)

        # Extract features
        print("Extracting features...")
        os.system('python3 SoundNet-tensorflow/extract_feat.py -m 17 -x 18 -s -p extract -t data.txt')

        # Load model and classify then return list of positives
        clf = AudioClassifier()
        probs = clf.predict('./output')
        print('Predictions', probs)

        start = chunk.get_chunk_position()[0]

        ret = []
        for i in range(len(probs)):
            if probs[i][1] > 0.6:
                ret.append(Highlight(start + i * 150, start + (i + 1) * 150, probs[i][1]))
        print('Found', len(ret), 'highlight(s).')
        return ret

    def generate_mp3(self, audio):
        n = len(audio)
        print('Audio Length =', n)

        if os.path.isdir(self.write_path):
            shutil.rmtree(self.write_path)
        os.mkdir(self.write_path)

        i = 0
        while i + self.window_size <= n:
            window = audio[i: i + self.window_size]
            window.export(self.write_path + str(i // self.window_size) +
                          ".mp3", format="mp3")
            i += self.window_size

    def generate_data_txt(self, n):
        f = open('data.txt', 'w')
        for i in range(n):
            f.write('./data/' + str(i) + '.mp3')
            if i < n-1: f.write('\n')
        f.close()
