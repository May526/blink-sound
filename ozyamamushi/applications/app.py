import os
import random
import sys
import time

import cv2
import IPython
import numpy as np
from playsound import playsound

from ozyamamushi import get_pj_root

freqs = [0] + [440.0 * 2.0 ** ((i - 9) / 12.0) for i in range(12)]
notes = ["R", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
dic = {}
for i, s in enumerate(notes):
    dic[s] = i


def play_mml(mml):
    rate = 48000
    BPM = 120
    qn_duration = 60.0 / BPM
    t = np.linspace(0.0, qn_duration, int(rate * qn_duration))
    music = np.array([])
    for s in list(mml):
        f = freqs[dic[s]]
        music = np.append(music, np.sin(2.0 * np.pi * f * t))
    return IPython.display.Audio(music, rate=rate, autoplay=True)


cascade_path = get_pj_root() + "/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml"
assert os.path.exists(cascade_path) is True
cascade = cv2.CascadeClassifier(cascade_path)

eye_cascade_path = get_pj_root() + "/venv/Lib/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml"
assert os.path.exists(eye_cascade_path) is True
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

blink_counter = 0
no_blink_counter = 0
no_blink_threshold = 5  # 5秒以上の瞬きのない閾値
last_blink_time = time.time()
l = [1, 2, 3, 4]

cap = cv2.VideoCapture(0)
while True:
    ret, rgb = cap.read()

    faces = []
    if ret is True:
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(
            gray, scaleFactor=1.11, minNeighbors=3, minSize=(100, 100)
        )

    if len(faces) == 1 and ret is True:
        x, y, w, h = faces[0, :]
        cv2.rectangle(rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # cv2.imwrite("face.jpg", rgb)

        # 処理高速化のために顔の上半分を検出対象範囲とする
        eyes_gray = gray[y : y + int(h / 2), x : x + w]
        eyes = eye_cascade.detectMultiScale(
            eyes_gray, scaleFactor=1.11, minNeighbors=3, minSize=(8, 8)
        )

        for ex, ey, ew, eh in eyes:
            cv2.rectangle(
                rgb, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 255, 0), 1
            )

        if len(eyes) == 0:
            blink_counter += 1
            no_blink_counter = 0
            last_blink_time = time.time()
            cv2.putText(
                rgb,
                "Blink!!",
                (10, 100),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
        else:
            no_blink_counter += 1

        # if no_blink_counter >= 5 * 10:  # 約5秒以上瞬きがなければ（15fpsで計算）
        if time.time() - last_blink_time > 5:
            sound_path = get_pj_root() + "\\data\\sounds\\剣で斬る1.mp3"
            playsound(sound_path)
            no_blink_counter = 0
        #     audio_num = random.choice(l)
        #     if audio_num == 1:
        #         playsound("./おーい　母.mp3")
        #     if audio_num == 2:
        #         playsound("./ねえねえ　母.mp3")
        #     if audio_num == 3:
        #         playsound("./今時間いい　兄.mp3")
        #     if audio_num == 4:
        #         playsound("./今時間大丈夫　兄.mp3")

        cv2.imshow("frame", rgb)
    if cv2.waitKey(1) == 27:
        break  # esc to quit

cap.release()
cv2.destroyAllWindows()

