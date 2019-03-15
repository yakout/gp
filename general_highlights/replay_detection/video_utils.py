import cv2
import config
import constant
import numpy as np
from ScoreboardDetector import ScoreboardDetector
from Scoreboard import Scoreboard
from matplotlib import pyplot as plt

def getCapturedFrames(video_filename):
    """Extract frames from video"""
    vidcap = cv2.VideoCapture(video_filename)
    success,image = vidcap.read()
    frames_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    captured_frames = []
    count = 0
    while success:
     	success,image = vidcap.read()
     	count+=1
     	if(success and np.random.randint(1, frames_count) <= constant.SIZE_OF_CAPTURED_FRAMES):
     	      captured_frames.append(image)
     	      print("captured_frame #:", len(captured_frames))

    print("total number of images ", count)

    return captured_frames


def labelFrames(video_filename, scoreboard):
    """Extract frames from video"""
    vidcap = cv2.VideoCapture(video_filename)
    success,image = vidcap.read()
    frames_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(config.OUTPUT_PATH + "scoreboard_liver.mp4", fourcc, fps, (width,height))
    video1 = cv2.VideoWriter(config.OUTPUT_PATH + "noscoreboard_liver.mp4", fourcc, fps, (width,height))

    countHasNotScoreboard = 0
    countHashScoreboard = 0
    while success:
     	success,image = vidcap.read()
     	if(success):
            if(scoreboard.hasScoreboard(image)):
                video.write(image)
                countHashScoreboard += 1
                print("scoreboard", countHashScoreboard)
            else:
                video1.write(image)
                countHasNotScoreboard += 1
                print("noscoreboard", countHasNotScoreboard)

        # cv2.destroyAllWindows()

    video1.release()
    video.release()
    vidcap.release()
    cv2.destroyAllWindows()
    return



file_path = config.INPUT_PATH + "Salah double keeps Reds top  Liverpool 4-3 Crystal Palace  Highlights.mp4"
# file_path = config.INPUT_PATH + "Egypt v Uruguay - 2018 FIFA World Cup Russia™ - MATCH 2.mp4"


captured_frames = getCapturedFrames(file_path)
scoreboardDetector = ScoreboardDetector(captured_frames)
x1, y1, x2, y2, scoreboards = scoreboardDetector.detectScoreboard()
scoreboard = Scoreboard(x1, y1, x2, y2, scoreboards)
labelFrames(file_path, scoreboard)


print(scoreboard.x1, " ", scoreboard.y1, " ", scoreboard.x2, " ", scoreboard.y2)
