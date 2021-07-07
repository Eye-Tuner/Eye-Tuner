"""ESC to terminate"""
# updated 2021.05.07
# last updated by MinJun Chang
# blink detection and csv file write added
# direction detection added

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


def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)],
                               np.int32)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)  # not in js
    cv2.fillPoly(mask, [left_eye_region], 255)  # not in js
    eye = cv2.bitwise_and(gray, gray, mask=mask)
    cv2.imshow('mask', mask)
    cv2.imshow('eye', eye)

    min_x = np.min(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_x = np.max(left_eye_region[:, 0])
    max_y = np.max(left_eye_region[:, 1])
    gray_eye = eye[min_y:max_y, min_x: max_x]
    # gray_left = cv2.cvtColor(left_eye, cv2.COLOR_BGR2GRAY)

    ########################################################
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    cv2.imshow('threshold_eye', threshold_eye)
    height, width = threshold_eye.shape
    threshold_left = threshold_eye[0: height, 0: int(width / 2)]
    threshold_right = threshold_eye[0: height, int(width / 2):width]
    white_left = cv2.countNonZero(threshold_left)
    white_right = cv2.countNonZero(threshold_right)

    if white_left == 0:
        gaze_ratio = 1
    elif white_right == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = white_left / white_right

    return gaze_ratio


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
        new_frame = np.zeros((500, 500, 3), np.uint8)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            # original #
            print(faces)
            x, y = face.left(), face.top()
            x1, y1 = face.right(), face.bottom()
            cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
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
            r_top_point = (round((landmarks.part(37).x + landmarks.part(38).x) / 2),
                           round((landmarks.part(37).y + landmarks.part(38).y) / 2))
            r_bot_point = (round((landmarks.part(40).x + landmarks.part(41).x) / 2),
                           round((landmarks.part(40).y + landmarks.part(41).y) / 2))

            l_left_point = (landmarks.part(42).x, landmarks.part(42).y)
            l_right_point = (landmarks.part(45).x, landmarks.part(45).y)
            l_top_point = (round((landmarks.part(43).x + landmarks.part(44).x) / 2),
                           round((landmarks.part(43).y + landmarks.part(44).y) / 2))
            l_bot_point = (round((landmarks.part(47).x + landmarks.part(46).x) / 2),
                           round((landmarks.part(47).y + landmarks.part(46).y) / 2))

            # r_hor_line = cv2.line(frame, r_left_point, r_right_point, (0,255,0), 2)
            # r_vert_line = cv2.line(frame, r_top_point,r_bot_point,(0,255,0),2)
            # l_hor_line = cv2.line(frame, l_left_point, l_right_point, (0, 255, 0), 2)
            # l_vert_line = cv2.line(frame, l_top_point, l_bot_point, (0, 255, 0), 2)

            r_vert_length = hypot((r_top_point[0] - r_bot_point[0]), (r_top_point[1] - r_bot_point[1]))
            l_vert_length = hypot((l_top_point[0] - l_bot_point[0]), (l_top_point[1] - l_bot_point[1]))
            r_hor_length = hypot((r_left_point[0] - r_right_point[0]), (r_left_point[1] - r_right_point[1]))
            l_hor_length = hypot((l_left_point[0] - l_right_point[0]), (l_left_point[1] - l_right_point[1]))

            r_ratio = r_hor_length / r_vert_length
            l_ratio = l_hor_length / l_vert_length

            r_coord = (
                round((landmarks.part(36).x + landmarks.part(39).x) / 2),
                round(
                    (round((landmarks.part(37).y + landmarks.part(38).y) / 2)) +
                    (round((landmarks.part(40).y + landmarks.part(41).y) / 2))
                )
            )
            l_coord = (round((landmarks.part(42).x + landmarks.part(45).x) / 2), round(
                (round((landmarks.part(43).y + landmarks.part(44).y) / 2)) + (
                    round((landmarks.part(46).y + landmarks.part(47).y) / 2))))

            if r_ratio >= 5.5 and l_ratio >= 5.5:
                cv2.putText(frame, "both blinking", (50, 150), font, 5, (0, 255, 0))
                right_blink_num = right_blink_num + 1
                left_blink_num = left_blink_num + 1
                tot_blink = right_blink_num + left_blink_num
            elif r_ratio >= 5.5 and l_ratio < 5.5:
                cv2.putText(frame, "right blinking", (50, 150), font, 5, (0, 255, 0))
                right_blink_num = right_blink_num + 1
                left_blink_num = left_blink_num
                tot_blink = right_blink_num + left_blink_num
            elif r_ratio < 5.5 and l_ratio >= 5.5:
                cv2.putText(frame, "left blinking", (50, 150), font, 5, (0, 255, 0))
                right_blink_num = right_blink_num
                left_blink_num = left_blink_num + 1
                tot_blink = right_blink_num + left_blink_num
            '''
            #Gaze Detection
            #여기부터 함수로 처리하고파...
            left_eye_region = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                                        (landmarks.part(37).x, landmarks.part(37).y),
                                        (landmarks.part(38).x, landmarks.part(38).y),
                                        (landmarks.part(39).x, landmarks.part(39).y),
                                        (landmarks.part(40).x, landmarks.part(40).y),
                                        (landmarks.part(41).x, landmarks.part(41).y)], np.int32)
            right_eye_region = np.array([(landmarks.part(42).x, landmarks.part(42).y),
                                        (landmarks.part(43).x, landmarks.part(43).y),
                                        (landmarks.part(44).x, landmarks.part(44).y),
                                        (landmarks.part(45).x, landmarks.part(45).y),
                                        (landmarks.part(46).x, landmarks.part(46).y),
                                        (landmarks.part(47).x, landmarks.part(47).y)], np.int32)

            height, width, _ = frame.shape
            mask = np.zeros((height, width), np.uint8)
            cv2.polylines(mask, [left_eye_region], True, 0, 1)
            cv2.polylines(mask, [right_eye_region], True, 0, 1)
            cv2.fillPoly(mask, [left_eye_region], 255)
            cv2.fillPoly(mask, [right_eye_region],255)
            eyeball = cv2.bitwise_and(gray, gray, mask = mask)

            l_min_x = np.min(left_eye_region[:, 0])
            l_min_y = np.min(left_eye_region[:, 1])
            l_max_x = np.max(left_eye_region[:, 0])
            l_max_y = np.max(left_eye_region[:, 1])
            left_eye = frame[l_min_y:l_max_y, l_min_x: l_max_x]
            gray_left = cv2.cvtColor(left_eye, cv2.COLOR_BGR2GRAY)
            r_min_x = np.min(right_eye_region[:, 0])
            r_min_y = np.min(right_eye_region[:, 1])

            r_max_x = np.max(right_eye_region[:, 0])
            r_max_y = np.max(right_eye_region[:, 1])
            right_eye = frame[r_min_y:r_max_y, r_min_x: r_max_x]
            gray_right = cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)
            ########################################################
            _, threshold_eye = cv2.threshold(gray_left, 70, 255, cv2.THRESH_BINARY)
            height, width = threshold_eye.shape
            threshold_left = threshold_eye[0: height, 0: int(width/2)]
            threshold_right = threshold_eye[0: height, int(width / 2):width]
            white_left = cv2.countNonZero(threshold_left)
            white_right = cv2.countNonZero(threshold_right)

            gaze_ratio = white_left/white_right
            cv2.putText(frame, str(gaze_ratio), (50, 100), font, 2, (0, 0, 255), 3)
            #cv2.putText(frame, str(white_left),(50,100), font, 2, (0,0,255),3)
            #cv2.putText(frame, str(white_right), (50, 150), font, 2, (0, 0, 255), 3)
            
            _, threshold_left = cv2.threshold(gray_left, 70,255,cv2.THRESH_BINARY)
            threshold_left = cv2.resize(threshold_left, None, fx = 5, fy = 5)
            left_eye = cv2.resize(left_eye, None, fx = 5, fy = 5)
            
            _, threshold_right = cv2.threshold(gray_right, 70, 255, cv2.THRESH_BINARY)
            threshold_right = cv2.resize(threshold_right, None, fx=5, fy=5)
            right_eye = cv2.resize(right_eye, None, fx=5, fy=5)
            '''
            ##########################################################
            # cv2.imshow("LeftEye",left_eye)
            # cv2.imshow("Thres_left", threshold_left)
            # cv2.imshow("Thres_right", threshold_right)
            # cv2.imshow("EyeGray", eyeball)
            gaze_ratio_left = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            gaze_ratio_right = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
            gaze_ratio = (gaze_ratio_right+gaze_ratio_left)/2

            if gaze_ratio <= 1:
                cv2.putText(frame, "RIGHT", (50,100), font,2,(0,0,255),3)
                new_frame[:] = (0,0,255)
            elif 1 < gaze_ratio < 3:
                cv2.putText(frame, "CENTER", (50, 100), font, 2, (0, 0, 255), 3)
            else:
                new_frame[:] = (255, 0, 0)
                cv2.putText(frame, "LEFT", (50, 100), font, 2, (0, 0, 255), 3)

            file.write(str(timer()) + "," + str(r_coord) + "," + str(l_coord) + "," + str(tot_blink) + "," + str(gaze_ratio) + "\n")
            file.flush()

        cv2.imshow("Frame", frame)
        cv2.imshow("NewFrame", new_frame)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
