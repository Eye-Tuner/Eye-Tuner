"""ESC to terminate"""
# updated 2021.04.24
# last updated by MinJun Chang
# csv file contents updated : time, coordinates of left and right eye centers

import cv2
import numpy as np
import dlib
import time
import os
import sys

DATA_DIR = (os.path.splitext(os.path.split(__file__)[1])[0] + '_' if '__file__' in globals() else '') + 'data'

# issue: [ WARN:1] global ... opencv\modules\videoio\src\cap_msmf.cpp (434) \
# `anonymous-namespace'::SourceReaderCB::~SourceReaderCB terminating async callback
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

if not sys.version_info >= (3, 8):
    timer = time.clock
if sys.platform == 'win32':
    timer = time.perf_counter
else:
    _timer_init = time.time()
    timer = lambda: time.time() - _timer_init  # noqa

data_dir = os.path.join(os.getcwd(), DATA_DIR)
if not os.path.exists(data_dir):
    os.mkdir(data_dir)
data_file = os.path.join(data_dir, "data_log_{}.csv".format(time.strftime('%Y_%m_%d_%H_%M_%S')))

with open(data_file, "a") as file:
    if os.stat(data_file).st_size == 0:
        file.write("TIME,X1,Y1,Z1,X2,Y2,Z2,X,Y,Z\n")  # todo: FILE CONTENTS

    while True:
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            # original #
            print(faces)
            x,y = face.left(), face.top()
            x1,y1= face.right(), face.bottom()
            cv2.rectangle(frame, (x,y),(x1,y1),(0,255,0),2)
            # end #

            landmarks = predictor(gray, face)
            # original #
            # print(landmarks.part(36))
            # x = landmarks.part(36).x
            # y = landmarks.part(36).y
            # cv2.circle(frame,(x,y),3,(0,0,255),1)
            # end #
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

            r_coord = (round((landmarks.part(36).x+landmarks.part(39).x)/2), round((round((landmarks.part(37).y +landmarks.part(38).y)/2))+(round((landmarks.part(40).y + landmarks.part(41).y)/2))))
            l_coord = (round((landmarks.part(42).x + landmarks.part(45).x) / 2), round((round((landmarks.part(43).y + landmarks.part(44).y) / 2)) + (round((landmarks.part(46).y + landmarks.part(47).y) / 2))))

            file.write(str(timer()) + "," + str(r_coord) + "," + str(l_coord) + "\n")
            file.flush()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


# Original contents:

# import cv2
# import numpy as np
# import dlib
# import time
# import os
#
# cap = cv2.VideoCapture(0)
#
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#
# abcde = time.time()
#         file = open("/home/pi/ws/0918/data/data_log_{}.csv".format(abcde), "a")
#         if os.stat("/home/pi/ws/0918/data/data_log_{}.csv".format(abcde)).st_size == 0:
#             file.write("TIME,X1,Y1,Z1,X2,Y2,Z2,X,Y,Z\n")
# while True:
#     _, frame = cap.read()
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     faces = detector(gray)
#     for face in faces:
#         #print(faces)
#         #x,y = face.left(), face.top()
#         #x1,y1= face.right(), face.bottom()
#         #cv2.rectangle(frame, (x,y),(x1,y1),(0,255,0),2)
#
#         landmarks = predictor(gray, face)
#         #print(landmarks.part(36))
#         #x = landmarks.part(36).x
#         #y = landmarks.part(36).y
#         #cv2.circle(frame,(x,y),3,(0,0,255),1)
#         r_left_point = (landmarks.part(36).x, landmarks.part(36).y)
#         r_right_point = (landmarks.part(39).x, landmarks.part(39).y)
#         r_top_point = (round((landmarks.part(37).x +landmarks.part(38).x)/2),round((landmarks.part(37).y +landmarks.part(38).y)/2))
#         r_bot_point = (round((landmarks.part(40).x + landmarks.part(41).x)/2), round((landmarks.part(40).y + landmarks.part(41).y)/2))
#
#         l_left_point = (landmarks.part(42).x, landmarks.part(42).y)
#         l_right_point = (landmarks.part(45).x, landmarks.part(45).y)
#         l_top_point = (round((landmarks.part(43).x + landmarks.part(44).x) / 2),round((landmarks.part(43).y + landmarks.part(44).y) / 2))
#         l_bot_point = (round((landmarks.part(47).x + landmarks.part(46).x) / 2),round((landmarks.part(47).y + landmarks.part(46).y) / 2))
#
#         r_hor_line = cv2.line(frame, r_left_point, r_right_point, (0,255,0), 2)
#         r_vert_line = cv2.line(frame, r_top_point,r_bot_point,(0,255,0),2)
#         l_hor_line = cv2.line(frame, l_left_point, l_right_point, (0, 255, 0), 2)
#         l_vert_line = cv2.line(frame, l_top_point, l_bot_point, (0, 255, 0), 2)
#
#         file.write(str(time.clock()) + "," + "\n")
#         file.flush()
#
#     cv2.imshow("Frame", frame)
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
# cap.release()
# cv2.destroyAllWindows()
