import cv2
import config
import constant
import numpy as np
from LogoDetector import LogoDetector
from Logo import Logo
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


file_path = config.PATH + "Egypt v Uruguay - 2018 FIFA World Cup Russia™ - MATCH 2.mp4"
captured_frames = getCapturedFrames(file_path)
logoDetector = LogoDetector(captured_frames)
x1, y1, x2, y2, img = logoDetector.detectLogo()
logo = Logo(x1, y1, x2, y2, img)

for img in captured_frames:
    if(logo.hasLogo(img)):
        plt.imshow(img, interpolation='nearest')
        plt.show()


print(logo.x1, " ", logo.y1, " ", logo.x2, " ", logo.y2)
