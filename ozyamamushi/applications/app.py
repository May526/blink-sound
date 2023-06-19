import os
import random
import sys
import time

import cv2
import numpy as np
import sounddevice as sd
import soundfile as sf
from playsound import playsound

from ozyamamushi import get_pj_root

sound_path = get_pj_root() + "\\data\\sounds\\剣で斬る1.mp3"
sound_path = sound_path.replace("\\", "/")
sig, sr = sf.read(sound_path, always_2d=True)
sd.play(sig, sr)

cascade_path = (
    get_pj_root() + "/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml"
)
assert os.path.exists(cascade_path) is True
cascade = cv2.CascadeClassifier(cascade_path)

eye_cascade_path = (
    get_pj_root()
    + "/venv/Lib/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml"
)
assert os.path.exists(eye_cascade_path) is True
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

blink_counter = 0
no_blink_counter = 0
no_blink_threshold = 5  # 5秒以上の瞬きのない閾値
last_blink_time = time.time()
l = [1, 2, 3, 4]
playing_sound = False
play_sound_start_time = 0

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
            if playing_sound is False:
                print("play sound")
                # playsound(sound_path, block=False)
                sig, sr = sf.read(sound_path, always_2d=True)
                sd.play(sig, sr)
                playing_sound = True
                play_sound_start_time = time.time()
            else:
                if time.time() - play_sound_start_time > 3:
                    playing_sound = False

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
