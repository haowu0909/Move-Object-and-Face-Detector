import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages")
#File Path
path = "/Users/wuhao/Desktop/Python - Udemy/App2/Face Detector/"

import cv2
import time
from datetime import datetime
import pandas

video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(path + "haarcascade_frontalface_default.xml")

while True:
    check, frame = video.read()

    gray_Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_Frame, 
    scaleFactor = 1.05, 
    minNeighbors = 5)

    for x,y,w,h in faces:
        frame = cv2.rectangle(frame, (x,y),(x+w, y+h), (0, 255,0), 3) #the last is the width of the line

    # add text
    cnt = len(faces)
    text = "Now " + str(cnt) + " faces in the recording"
    cv2.putText(frame, text, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    cv2.imshow("Face Detector", frame)

    key = cv2.waitKey(10)
    if key == ord('q'):  #break the loop
        break

video.release() # close the camera
cv2.destroyAllWindows()
print("the app has been closed")