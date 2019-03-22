from abc import ABC, abstractmethod
import sys
import shutil
import os
from classifier import *
from video_model import Highlight, Chunk
from component import Component, ComponentContainer

class SoundComponent(Component):

    def __init__(self):
        ComponentContainer.register_component('sound', self)

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

        self.generate_data_txt(len(audio))

        # Extract features
        os.system('python extract_feat.py -m 17 -x 18 -s -p extract -t data.txt')

        # Load model and classify then return list of positives
        clf = AudioClassifier()
        predictions, probs = clf.predict('./output')

    def generate_mp3(self, audio):
        n = len(audio)

        window_size = 6000  # 6 seconds sample size
        write_path = "data/"

        if os.path.isdir(write_path):
            shutil.rmtree(write_path)
        os.mkdir(write_path)

        i = 0
        while i + window_size <= n:
            window = audio[i: i + window_size]
            window.export(write_path + str(i // window_size) +
                          ".mp3", format="mp3")
            i += window_size

    def generate_data_txt(self, n):
        f = open('data.txt', 'w')
        for i in range(n):
            f.write('./data/' + str(i) + '.mp3')
        f.close()
