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
  	  	# cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
     	success,image = vidcap.read()
     	# print('Read a new frame: ', count, success)
     	if(success and np.random.randint(1, frames_count) <= constant.SIZE_OF_CAPTURED_FRAMES):
     	      captured_frames.append(image)
     	      print("captured_frame #:", len(captured_frames))

    return captured_frames


file_path = config.PATH + "Salah double keeps Reds top  Liverpool 4-3 Crystal Palace  Highlights.mp4"
file_path = config.PATH + "Egypt v Uruguay - 2018 FIFA World Cup Russia™ - MATCH 2.mp4"
captured_frames = getCapturedFrames(file_path)
scoreboardDetector = ScoreboardDetector(captured_frames)
x1, y1, x2, y2, scoreboards = scoreboardDetector.detectScoreboard()
scoreboard = Scoreboard(x1, y1, x2, y2, scoreboards)

print("number of scoreboards", len(scoreboards))
countHasScoreboard = 0
for img in captured_frames:
    if(scoreboard.hasScoreboard(img)):
        countHasScoreboard += 1
        if countHasScoreboard % 10 == 0:
          print("has scoreboard", countHasScoreboard)
          plt.figure()
          plt.imshow(img[x1:x2+1, y1:y2+1, :], interpolation='nearest')
          plt.show()



print(scoreboard.x1, " ", scoreboard.y1, " ", scoreboard.x2, " ", scoreboard.y2)
