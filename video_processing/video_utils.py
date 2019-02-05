import cv2
import config
import constant

def getCapturedFrames(video_filename):
    """Extract frames from video"""
    vidcap = cv2.VideoCapture(video_filename)
    success,image = vidcap.read()
    frames_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)

    captured_frames = []
    while success:
  	  # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
     	success,image = vidcap.read()
     	# print('Read a new frame: ', count, success)
     	if(randint(1, frames_count) <= constant.SIZE_OF_CAPTURED_FRAMES):
  		captured_frames.append(image)
  	   	print("captured_frame #:", len(captured_frame))

    return captured_frames


file_path = config.PATH + "SampleVideo_1280x720_1mb.mp4"
getCapturedFrames(file_path)
# to stage