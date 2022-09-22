import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages")
#File Path
path = "/Users/wuhao/Desktop/Python - Udemy/App2/"

import cv2
import time
from datetime import datetime
import pandas

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns = ["Start", "End"])

video = cv2.VideoCapture(0)
# some webcam cannot capture the first frame staticlly, so delay si needed
video.read() 
time.sleep(2)

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #blur the image, remove noise and increase the accuracy
    gray = cv2.GaussianBlur(gray, (21,21), 0) 

    if first_frame is None:
        first_frame = gray
        continue
    
    #comapre difference from the last frame
    delta_frame = cv2.absdiff(first_frame, gray)
    # compare the first frame when the difference is greater than 30
    thresh_frame = cv2.threshold(delta_frame, 30,255, cv2.THRESH_BINARY)[1]

    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    # draw contours in the image
    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # filter contours
    for contour in cnts:
        if cv2.contourArea(contour) < 50000:
            continue
        status = 1
        
        (x,y,w,h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
    # add text
    cv2.putText(frame, 'Warning: You are under camera !!!', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    status_list.append(status)
    # # only save the last two element in array, to save memory
    # if len(status_list) >= 2:
    #     status_list.remove(status_list[0])
    #     status_list.append(status)


    # each time motion starts occurs, record the time
    # one start time and one end time
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())


    # cv2.imshow("Gray Frame", gray)
    # cv2.imshow("Delta Frame", delta_frame)
    # cv2.imshow("Threshhold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):  #break the loop
        # record the end time if the last status is motion
        if status == 1:
            times.append(datetime.now())
        # print('the record has been stopped')
        break

# print(times)
for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index = True)

print("next bug &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
df.to_csv(path + "Times.csv")
video.release() # close the camera
cv2.destroyAllWindows()