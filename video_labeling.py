from video_processing import VideoChunkReader
import config
from moviepy.editor import VideoFileClip, concatenate_videoclips
import time

video_name = "egy-uru-0-1"

video_reader = VideoChunkReader(config.INPUT_PATH + video_name + ".mp4", 0)


count = 0
f = open(config.TRAINNING_OUTPUT_PATH + video_name + ".txt", "w")

shot_length = 0
while(video_reader.has_next()):
    chunk = video_reader.get_next()
    # newclip = chunk.get_clip().fl_time(lambda: 3-t)
    chunk.get_clip().preview()
    # if(shot_length < 10):
    #     shot_length += chunk.get_clip().duration
    #     continue
    # else:
    #     shot_length = 0
    count += 1

    print("clip count: ", count)
    type = -1
    # while(type != 0 and type != 1):
    #     type = int(input("Enter a type of clip: "))
    #     # print(type(type))
    #     if(type != 0 and type != 1):
    #         print("y3l2 d5l 0 or 1 :D")
    time.sleep(1)
    # f.write(str(type) + "\n")


f.close()
