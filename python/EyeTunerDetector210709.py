"""ESC to terminate"""
# updated 2021.07.09
# last updated by Dongha Kim
# blink counter bundled
# uses function

import os
import sys

import math
import time

import contextlib
import cv2
import dlib
import numpy as np


def get_eye_length(eye_coordinates):
    left_point = [eye_coordinates[0].x, eye_coordinates[0].y]
    right_point = [eye_coordinates[3].x, eye_coordinates[3].y]
    top_point = [(eye_coordinates[1].x + eye_coordinates[2].x) / 2,
                 (eye_coordinates[1].y + eye_coordinates[2].y) / 2]
    bot_point = [(eye_coordinates[4].x + eye_coordinates[5].x) / 2,
                 (eye_coordinates[4].y + eye_coordinates[5].y) / 2]
    hor_length = math.hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    vert_length = math.hypot((top_point[0] - bot_point[0]), (top_point[1] - bot_point[1]))
    return hor_length, vert_length


def get_eye_center(eye_coordinates):
    return (
        round((eye_coordinates[0].x + eye_coordinates[3].x) / 2),
        round(
            ((eye_coordinates[1].y + eye_coordinates[2].y) / 2) +
            ((eye_coordinates[4].y + eye_coordinates[5].y) / 2)
        )
    )


def get_eye_from_matrix(mat, eye_coordinates, convert_color=False):
    if convert_color:
        mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)
    height, width, *_ = mat.shape
    mask = np.zeros((height, width), np.uint8)
    eye_array = np.array([(p.x, p.y) for p in eye_coordinates], np.int32)
    cv2.polylines(mask, [eye_array], True, 255, 2)  # not in js
    cv2.fillPoly(mask, [eye_array], 255)  # not in js
    return cv2.bitwise_and(mat, mat, mask=mask)[
        np.min(eye_array[:, 1]):np.max(eye_array[:, 1]),  # min_y:max_y
        np.min(eye_array[:, 0]):np.max(eye_array[:, 0]),  # min_x:max_x
    ]


def get_gaze_ratio(mat, eye_coordinates, thresh_show_dst=None, convert_color=False):

    eye = get_eye_from_matrix(mat, eye_coordinates, convert_color=convert_color)

    _, eye = cv2.threshold(eye, 70, 255, cv2.THRESH_BINARY)

    if thresh_show_dst is not None:
        cv2.imshow(thresh_show_dst, eye)

    height, width, *_ = eye.shape
    threshold_left = eye[0: height, 0: int(width / 2)]
    threshold_right = eye[0: height, int(width / 2):width]
    white_left = cv2.countNonZero(threshold_left)
    white_right = cv2.countNonZero(threshold_right)

    if white_left == 0:
        gaze_ratio = 1
    elif white_right == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = white_left / white_right
    return gaze_ratio


def get_blinking_ratio(eye_coordinates):
    hor_length, vert_length = get_eye_length(eye_coordinates)
    return hor_length / vert_length if vert_length else math.inf


def get_timer():
    if not sys.version_info >= (3, 8):
        return time.clock
    if sys.platform == 'win32':
        return time.perf_counter
    else:
        _timer_init = time.time()
        return lambda: time.time() - _timer_init


@contextlib.contextmanager
def writer(
        filename,
        header=None,
        *,
        directory=None,
):
    if directory is not None:
        directory = os.path.abspath(directory)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        filename = os.path.join(directory, filename)
    with open(filename, "a") as file:
        if os.stat(filename).st_size == 0 and header is not None:
            file.write(header)
            file.flush()
        yield file


if __name__ == '__main__':

    # Init video capture
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Init detectors
    detector = dlib.get_frontal_face_detector()  # noqa
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # noqa

    # Init CSV
    with writer(
        header="TIME,r_coordinate,l_coordinate,right_blink,left_blink,total_blink,gaze_ratio\n",
        filename="data_log_%s.csv" % time.strftime('%Y_%m_%d_%H_%M_%S'),
        directory=os.path.splitext(os.path.split(__file__)[1])[0] + '_data',
    ) as csv:

        # Init timer
        timer = get_timer()

        font = cv2.FONT_HERSHEY_PLAIN

        # Blink variables
        right_blink_num = 0
        left_blink_num = 0

        while True:
            _, frame = cap.read()
            new_frame = np.zeros((500, 500, 3), np.uint8)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)

            for face in faces:

                # Draw rectangle
                cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

                landmarks = predictor(gray, face).parts()
                right_eye = landmarks[36:42]
                left_eye = landmarks[42:48]

                r_coord = get_eye_center(right_eye)
                l_coord = get_eye_center(left_eye)

                blink_ratio_r = get_blinking_ratio(right_eye)
                blink_ratio_l = get_blinking_ratio(left_eye)

                gaze_ratio_r = get_gaze_ratio(gray, right_eye, thresh_show_dst='threshold_eye_right')
                gaze_ratio_l = get_gaze_ratio(gray, left_eye, thresh_show_dst='threshold_eye_left')
                gaze_ratio = (gaze_ratio_r + gaze_ratio_l) / 2

                if blink_ratio_r >= 5.5 and blink_ratio_l >= 5.5:
                    cv2.putText(frame, "both blinking", (50, 150), font, 5, (0, 255, 0))
                    right_blink_num += 1
                    left_blink_num += 1
                elif blink_ratio_r >= 5.5 and blink_ratio_l < 5.5:
                    cv2.putText(frame, "right blinking", (50, 150), font, 5, (0, 255, 0))
                    right_blink_num += 1
                elif blink_ratio_r < 5.5 and blink_ratio_l >= 5.5:
                    cv2.putText(frame, "left blinking", (50, 150), font, 5, (0, 255, 0))
                    left_blink_num += 1

                if gaze_ratio <= 1:
                    cv2.putText(frame, "RIGHT", (50,100), font, 2, (0, 0, 255), 3)
                    new_frame[:] = (0, 0, 255)
                elif 1 < gaze_ratio < 3:
                    cv2.putText(frame, "CENTER", (50, 100), font, 2, (0, 0, 255), 3)
                else:
                    new_frame[:] = (255, 0, 0)
                    cv2.putText(frame, "LEFT", (50, 100), font, 2, (0, 0, 255), 3)

                data = [
                    timer(),
                    '%s-%s' % r_coord, '%s-%s' % l_coord,
                    right_blink_num, left_blink_num, right_blink_num + left_blink_num,
                    round(gaze_ratio, 4)
                ]
                csv.write(",".join(map(str, data)))
                csv.write("\n")
                csv.flush()

            cv2.imshow("Frame", frame)
            cv2.imshow("NewFrame", new_frame)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break

        cap.release()
        cv2.destroyAllWindows()
