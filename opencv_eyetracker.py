import cv2
import numpy as np
import dlib
import time
import os

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        #print(faces)
        #x,y = face.left(), face.top()
        #x1,y1= face.right(), face.bottom()
        #cv2.rectangle(frame, (x,y),(x1,y1),(0,255,0),2)

        landmarks = predictor(gray, face)
        #print(landmarks.part(36))
        #x = landmarks.part(36).x
        #y = landmarks.part(36).y
        #cv2.circle(frame,(x,y),3,(0,0,255),1)
        r_left_point = (landmarks.part(36).x, landmarks.part(36).y)
        r_right_point = (landmarks.part(39).x, landmarks.part(39).y)
        r_top_point = (round((landmarks.part(37).x +landmarks.part(38).x)/2),round((landmarks.part(37).y +landmarks.part(38).y)/2))
        r_bot_point = (round((landmarks.part(40).x + landmarks.part(41).x)/2), round((landmarks.part(40).y + landmarks.part(41).y)/2))

        l_left_point = (landmarks.part(42).x, landmarks.part(42).y)
        l_right_point = (landmarks.part(45).x, landmarks.part(45).y)
        l_top_point = (round((landmarks.part(43).x + landmarks.part(44).x) / 2),round((landmarks.part(43).y + landmarks.part(44).y) / 2))
        l_bot_point = (round((landmarks.part(47).x + landmarks.part(46).x) / 2),round((landmarks.part(47).y + landmarks.part(46).y) / 2))

        r_hor_line = cv2.line(frame, r_left_point, r_right_point, (0,255,0), 2)
        r_vert_line = cv2.line(frame, r_top_point,r_bot_point,(0,255,0),2)
        l_hor_line = cv2.line(frame, l_left_point, l_right_point, (0, 255, 0), 2)
        l_vert_line = cv2.line(frame, l_top_point, l_bot_point, (0, 255, 0), 2)

        '''file.write(str(time.clock()) + "," + "\n")
        file.flush()'''

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
