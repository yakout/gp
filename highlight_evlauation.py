from video_processing import VideoChunkReader
import config
from moviepy.editor import *
import time
import cv2

video_name = "Tottenham vs Ajax 0-1 - Extended Highlights 2019 HD"

video_reader = VideoChunkReader("general_highlights/replay_detection/video_processing/videos/" + video_name + ".mp4", 0)


count = 0
f = open("evaluation_data/" + video_name + ".txt", "w")

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

    while(type >= 0 and type <= 5):
        try:
            type = int(input("Enter a type of clip: "))
        except:
            type = -1

        # print(type(type))
        if(type < 0 or type > 5):
            print("y3l2 d5l integer from 0 to 5 :D")

    # time.sleep(.5)
    f.write(str(type) + "\n")



f.close()
