import cv2

def video_to_frames(video_filename):
    """Extract frames from video"""
    vidcap = cv2.VideoCapture(video_filename)
    success,image = vidcap.read()
    count = 0
    while success:
      # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
      success,image = vidcap.read()
      # print('Read a new frame: ', count, success)
      count += 1

file_path = "/home/ahmednagga19/Downloads/bar-mad-sc.avi"
video_to_frames(file_path)