import numpy as np
import cv2

# Cascades 디렉토리의 haarcascade_frontalface_default.xml 파일을 Classifier로 사용
faceCascade = cv2.CascadeClassifier('haarcascade_frontface.xml')
eyeCascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')

#웹캠에서 영상을 읽어옴
cap = cv2.VideoCapture(0)
cap.set(3, 640) #WIDTH
cap.set(4, 480) #HEIGHT

while(True) :
    
    # frame 별로 capture 한다
    ret, frame = cap.read()
    frame = cv2.flip(frame,1) # Flip camera vertically
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )


    for( x,y,w,h ) in faces :
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]

        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=10,
            minSize=(5, 5)
        )
        for( ex,ey,ew,eh) in eyes :
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()