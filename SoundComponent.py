from abc import ABC, abstractmethod
import sys
import shutil
import time
import os
import secrets
from classifier import AudioClassifier
from video_model import Highlight, Chunk
from component import Component, ComponentContainer
import threading
import shutil


class SoundComponent(Component):
    """
    Data folder structure for the input data that will be used by SoundNet
    ./data/:random_hash/mp3/0.mp3
                       |   /1.mp3
                       |   /...
                       /data.txt
    Output folder structure for output data produced by SoundNet
    ./output/:random_hash/0.npy
                         /1.npy
                         /2.npy
    """
    def __init__(self):
        self.write_path = './data/'
        self.data_paths_file_name = 'data.txt'
        self.sound_net_output_folder = './output/'
        self.window_size = 6000  # 6 sec window
        self._init_locks()

        # Clean and delete old data
        if os.path.isdir(self.write_path):
            shutil.rmtree(self.write_path)

        if os.path.isdir(self.sound_net_output_folder):
            shutil.rmtree(self.sound_net_output_folder)

        # Creating needed directories
        os.mkdir(self.write_path)
        os.mkdir(self.sound_net_output_folder)

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
        window_size_in_sec = int(self.window_size / 1000)
        # print("audio duration {}".format(audio.duration))
        if audio.duration < window_size_in_sec:
            return []

        unique_hash            = self._generate_mp3(audio)
        unique_path            = self.write_path + unique_hash
        features_output_folder = self.sound_net_output_folder + unique_hash

        # TODO: check that int(audio.duration) will not cause any numeric issues
        self._generate_data_txt(unique_path, int(audio.duration) // window_size_in_sec)

        # Extract features
        print("Extracting target data features...")
        os.system(
            "python SoundNet-tensorflow/extract_feat.py -m 17 -x 18 -s -p extract -t {} --outpath {}".format(
                unique_path + '/' + self.data_paths_file_name,
                features_output_folder
            )
        )

        # Load model and classify then return list of positives
        clf = AudioClassifier(self.sound_locks['training_lock'])
        probs = clf.predict(features_output_folder)
        #print('Predictions', probs)

        start = chunk.get_chunk_position()[0]
        frame_per_sample = window_size_in_sec * chunk.get_fps()
        ret = []
        for i in range(len(probs)):
            if probs[i][1] > 0.8:
                ret.append(Highlight(start + i * frame_per_sample,
                                     start + (i + 1) * frame_per_sample, probs[i][1]))
        print("Sound Component: highlights length returned: {}".format(len(ret)))
        return ret

    # generate mp3 using moviepy
    def _generate_mp3(self, audio):
        n = audio.duration # total duration in seconds

        unique_hash = secrets.token_hex(5)
        unique_path = self.write_path + unique_hash

        if os.path.isdir(unique_path):
            shutil.rmtree(unique_path)
        os.mkdir(unique_path)

        window_size_in_sec = int(self.window_size / 1000)
        i = 0

        while i + window_size_in_sec <= n: # ignore the small trainling sample
            # print("subclip audio file between: {} and {}".format(i, i + window_size_in_sec))
            audio.subclip(i, i + window_size_in_sec).write_audiofile(
                unique_path + '/' + str(i // window_size_in_sec) + ".mp3",
                verbose=False,
                logger=None
            )
            i += window_size_in_sec

        return unique_hash

    def _generate_data_txt(self, unique_path, n):
        f = open(unique_path + '/' + self.data_paths_file_name, 'w')
        for i in range(n):
            f.write(unique_path + '/' + str(i) + '.mp3')
            if i < n - 1:
                f.write('\n')
        f.close()

    def _init_locks(self):
        self.sound_locks = {}
        self.sound_locks['training_lock'] = threading.Lock()
