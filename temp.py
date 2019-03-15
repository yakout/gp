import cv2
import numpy as np
import config
import constant
from numpy import linalg as LA
import ZeroCrossing as zc

def detetMotion(video_filename):
    video_capture = cv2.VideoCapture(video_filename)

    # Read two frames, last and current, and convert current to gray.
    ret, last_frame = video_capture.read()
    ret, current_frame = video_capture.read()
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    width, height, depth = current_frame.shape
    size = width*height*depth
    frames_count = 1
    window_count = 0
    window = []

    negro_window = []
    while(True):
        # We want two frames- last and current, so that we can calculate the different between them.
        # Store the current frame as last_frame, and then read a new one
        last_frame = current_frame
        ret, current_frame = video_capture.read()
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Find the absolute difference between frames
        d = LA.norm(cv2.absdiff(last_frame, current_frame))/size

        # print(d)
        window.append(d)
        # if(frames_count%constant.WINDOW_SIZE == 0):
        #     window_count += 1
        #     print("New Window", window_count)
        #     print("mean" , np.mean(window))
        #     print("median" , np.median(window))
        #     print("variance", np.var(window))
        #     print("less than threshold", len(np.where(np.array(window) < 10000)))
        #     window = []

        # if(d > 50000):
        #     if(len(negro_window) < 100):
        #         negro_window = []
        #         continue
        #     print("\nnew negro window")
        #     print("mean" , np.mean(negro_window))
        #     print("median" , np.median(negro_window))
        #     print("variance", np.sqrt(np.var(negro_window)))
        #     print("length", len(negro_window))
        #     print("less than threshold", len(np.where(np.array(negro_window) < 50000)))
        #     negro_window = []
        # else:
        #     negro_window.append(d)

        print(zc.getZeroCrossingTheta_pzc(frames_count, window))
        frames_count += 1
        cv2.imshow('Video',current_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


file_path = config.INPUT_PATH + "This Channel will be terminated. Please subscribe our second channel.The link is below.mp4"
detetMotion(file_path);
