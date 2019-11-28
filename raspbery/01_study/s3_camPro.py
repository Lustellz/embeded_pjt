import numpy as np
import cv2

#웹캠에서 영상을 읽어옴
cap = cv2.VideoCapture(0)
cap.set(3, 640) #WIDTH
cap.set(4, 480) #HEIGHT

while(True) :
    
    # frame 별로 capture 한다
    ret, frame = cap.read()
    frame = cv2.flip(frame,1) # Flip camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()