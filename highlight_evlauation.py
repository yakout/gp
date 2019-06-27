from video_processing import VideoChunkReader
from moviepy.editor import *
import time
import cv2

true_path = "true/"
false_path = "false/"

for video_name in ["handball_cliip"]:

    video_reader = VideoChunkReader(video_name + ".mp4")
    count = 500

    shot_length = 0
    while(video_reader.has_next()):
        chunk = video_reader.get_next()

        type = -1
        count += 1

        print("clip count: ", count)

        if(chunk.get_frames_count() >= 2):
            chunk.get_clip().preview()
        else:
            type = 0

        while(type < 0 or type > 1):
            try:
                type = int(input("Enter a type of clip: "))
            except:
                type = -1

            # print(type(type))
            if(type < 0 or type > 1):
                print("y3l2 d5l integer from 0 to 1 :D")

            if(type == 1):
                chunk.get_audio().write_audiofile(true_path + str(count) + '.mp3')
            elif(type == 0):
                chunk.get_audio().write_audiofile(false_path + str(count) + '.mp3')
