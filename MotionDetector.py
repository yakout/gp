import cv2
import numpy as np
import config


def detetMotion(video_filename):
    video_capture = cv2.VideoCapture(video_filename)

    # Read two frames, last and current, and convert current to gray.
    ret, last_frame = video_capture.read()
    ret, current_frame = video_capture.read()
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    frames_count = 0
    motion_frame = 0
    while(True):
        # We want two frames- last and current, so that we can calculate the different between them.
        # Store the current frame as last_frame, and then read a new one
        last_frame = current_frame
        ret, current_frame = video_capture.read()
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Find the absolute difference between frames
        diff = cv2.absdiff(last_frame, current_frame)


        # Uncomment the below to see the difference values
        frames_count += 1
        if frames_count % 10 == 0:
            # frames_count = 0
            # print ("currnet frame:", np.mean(current_frame))
            # print ("diff:" , np.mean(diff))


            # If difference is greater than a threshold, that means motion detected.
            if np.mean(diff) > 10:
                motion_frame += 1
                print("Achtung! Motion detected.")
                print("motion frame: ", motion_frame, " frame number: ", frames_count)


        # Display the resulting frame
        cv2.imshow('Video',diff)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


file_path = config.INPUT_PATH + "Salah double keeps Reds top  Liverpool 4-3 Crystal Palace  Highlights.mp4"
detetMotion(file_path);
