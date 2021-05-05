"""ESC to terminate"""
# updated 2021.05.05
# last updated by MinJun Chang
# blink detection and csv file write added

import cv2
import numpy as np
import dlib
import time
import os
import sys
from math import hypot

DATA_DIR = (os.path.splitext(os.path.split(__file__)[1])[0] + '_' if '__file__' in globals() else '') + 'data'

# issue: [ WARN:1] global ... opencv\modules\videoio\src\cap_msmf.cpp (434) \
# `anonymous-namespace'::SourceReaderCB::~SourceReaderCB terminating async callback
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_PLAIN
right_blink_num = 0
left_blink_num = 0
tot_blink = 0

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
        file.write("TIME,r_coordinate, ,l_coordinate, , blink\n")  # todo: FILE CONTENTS

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

            r_vert_length = hypot((r_top_point[0] - r_bot_point[0]),(r_top_point[1] - r_bot_point[1]))
            l_vert_length = hypot((l_top_point[0] - l_bot_point[0]),(l_top_point[1] - l_bot_point[1]))
            r_hor_length = hypot((r_left_point[0] - r_right_point[0]),(r_left_point[1] - r_right_point[1]))
            l_hor_length = hypot((l_left_point[0] - l_right_point[0]),(l_left_point[1] - l_right_point[1]))

            r_ratio = r_hor_length/r_vert_length
            l_ratio = l_hor_length/l_vert_length

            r_coord = (round((landmarks.part(36).x+landmarks.part(39).x)/2), round((round((landmarks.part(37).y +landmarks.part(38).y)/2))+(round((landmarks.part(40).y + landmarks.part(41).y)/2))))
            l_coord = (round((landmarks.part(42).x + landmarks.part(45).x) / 2), round((round((landmarks.part(43).y + landmarks.part(44).y) / 2)) + (round((landmarks.part(46).y + landmarks.part(47).y) / 2))))

            if r_ratio >= 5.5 and l_ratio >= 5.5:
                cv2.putText(frame, "both blinking", (50,150), font, 5, (0,255,0))
                right_blink_num = right_blink_num+1
                left_blink_num = left_blink_num+1
                tot_blink = right_blink_num+left_blink_num
            elif r_ratio >= 5.5 and l_ratio < 5.5:
                cv2.putText(frame, "right blinking", (50, 150), font,5, (0, 255, 0))
                right_blink_num = right_blink_num + 1
                left_blink_num = left_blink_num
                tot_blink = right_blink_num + left_blink_num
            elif r_ratio < 5.5 and l_ratio >= 5.5:
                cv2.putText(frame, "left blinking", (50, 150), font, 5, (0,255, 0))
                right_blink_num = right_blink_num
                left_blink_num = left_blink_num +1
                tot_blink = right_blink_num + left_blink_num

            #Gaze Detection
            left_eye_region = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                                        (landmarks.part(37).x, landmarks.part(37).y),
                                        (landmarks.part(38).x, landmarks.part(38).y),
                                        (landmarks.part(39).x, landmarks.part(39).y),
                                        (landmarks.part(40).x, landmarks.part(40).y),
                                        (landmarks.part(41).x, landmarks.part(41).y)], np.int32)

            height, width, _ = frame.shape
            mask = np.zeros((height, width), np.uint8)
            cv2.polylines(mask, [left_eye_region], True, 255, 2)
            cv2.fillPoly(mask, [left_eye_region], 255)
            left_eyeball = cv2.bitwise_and(gray, gray, mask = mask)

            l_min_x = np.min(left_eye_region[:, 0])
            l_min_y = np.min(left_eye_region[:, 1])
            l_max_x = np.max(left_eye_region[:, 0])
            l_max_y = np.max(left_eye_region[:, 1])
            left_eye = frame[l_min_y:l_max_y, l_min_x: l_max_x]
            gray_left = cv2.cvtColor(left_eye, cv2.COLOR_BGR2GRAY)
            _, threshold_left = cv2.threshold(gray_left, 70,255,cv2.THRESH_BINARY)
            threshold_left = cv2.resize(threshold_left, None, fx = 5, fy = 5)
            left_eye = cv2.resize(left_eye, None, fx = 5, fy = 5)
            cv2.imshow("LeftEye",left_eye)
            cv2.imshow("Thres", threshold_left)
            cv2.imshow("LeftEyeGray", left_eyeball)


            file.write(str(timer()) + "," + str(r_coord) + "," + str(l_coord) + "," + str(tot_blink)+ "\n")
            file.flush()

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()