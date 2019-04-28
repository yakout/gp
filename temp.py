import numpy as np
import cv2

cap = cv2.VideoCapture("/Users/ahmed/Desktop/GP/gp/videos/Liverpool vs Porto 2 0 Goals and Highlights 2019 HD.mp4")
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()        
    
    # Our operations on the frame come here    
    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(frame,cv2.COLOR_RGB2Luv)   # BGR color to gray level
    print(img.shape)
    # Display the resulting image
    sumImg = np.mean(img, axis=(0,1))
    print(sumImg)
    print(sumImg.shape)
    cv2.imshow('Gray',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
        break
        
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()