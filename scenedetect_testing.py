from video_processing import VideoChunkReader
from scenedetector import *
import config
# from moviepy.editor import *
import time
import cv2

import moviepy.editor as mpe
from moviepy.editor import concatenate_videoclips


video_name = "barca - RM  5 - 0"

video_clip = mpe.VideoFileClip(config.INPUT_PATH + video_name + ".mp4")
bounds = find_scenes(config.INPUT_PATH + video_name + ".mp4")


count = 0
# f = open(config.TRAINNING_OUTPUT_PATH + video_name + ".txt", "w")

shot_length = 0
last_bound = 0

for bound in bounds:
    chunk = video_clip.copy().subclip(last_bound, bound).copy()
    number_of_frames = int(chunk.fps * chunk.duration)

    # if(shot_length < 10):
    #     shot_length += chunk.get_clip().duration
    #     continue
    # else:
    #     shot_length = 0

    type = -1
    count += 1

    print("clip count: ", count)


    if(number_of_frames >= 2):
        chunk.preview()
    else:
        type = 0

    # while(type != 0 and type != 1):
    #     try:
    #         type = int(input("Enter a type of clip: "))
    #     except:
    #         type = -1
    #
    #     # print(type(type))
    #     if(type != 0 and type != 1):
    #         print("y3l2 d5l 0 or 1 :D")

    time.sleep(.5)
    # f.write(str(type) + "\n")
    last_bound = bound


# f.close()
