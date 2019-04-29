from video_processing import VideoChunkReader
import config
from moviepy.editor import *
import time
import cv2

video_name = "barca - bayrn  3 - 0"

video_reader = VideoChunkReader(config.INPUT_PATH + video_name + ".mp4", 0)


count = 0
f = open(config.TRAINNING_OUTPUT_PATH + video_name + ".txt", "w")

shot_length = 0
while(video_reader.has_next()):
    chunk = video_reader.get_next()

    # if(shot_length < 10):
    #     shot_length += chunk.get_clip().duration
    #     continue
    # else:
    #     shot_length = 0

    type = -1
    count += 1

    print("clip count: ", count)

    if(chunk.get_frames_count() >= 2):
        chunk.get_clip().preview()
    else:
        type = 0

    while(type != 0 and type != 1):
        try:
            type = int(input("Enter a type of clip: "))
        except:
            type = -1

        # print(type(type))
        if(type != 0 and type != 1):
            print("y3l2 d5l 0 or 1 :D")

    # time.sleep(3)
    f.write(str(type) + "\n")



f.close()
