import os
import sys
import time
import datetime

import cv2
import sounddevice as sd
import soundfile as sf
from playsound import playsound
import csv
import glob

import tkinter as tk
from concurrent.futures import ProcessPoolExecutor

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from ozyamamushi import get_pj_root

sound_path_list = glob.glob(get_pj_root() + "/applications/data/sounds/kanai_ozyama_sound"+"/*")

cap = cv2.VideoCapture(0)

cascade_path = (
    get_pj_root() + "/applications/venv/lib/python3.10/site-packages/cv2/data/haarcascade_frontalface_alt2.xml"
)

print(cascade_path)

assert os.path.exists(cascade_path) is True
cascade = cv2.CascadeClassifier(cascade_path)

eye_cascade_path = (
    get_pj_root()
    + "/applications/venv/lib/python3.10/site-packages/cv2/data/haarcascade_eye_tree_eyeglasses.xml"
)

assert os.path.exists(eye_cascade_path) is True
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

def subrepo():
    subjective_report = []
    root = tk.Tk()
    root.geometry("500x300")

    entry = tk.Entry()
    entry.place(x=20, y=50)
    subrepo_start_time = datetime.datetime.now()

    def click():
        rate = entry.get()
        subjective_report.append([datetime.datetime.now(),rate.split(",")])
        entry.delete(0, tk.END)
        with open('./data/'+str(subrepo_start_time)+'_subjectivereport_sample.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["time","annoyed(1~10)","surprised(1~10)","horror(1~10)","concentrating(1~10)"])
            for n in range(len(subjective_report)):
                writer.writerow(subjective_report[n])

    label = tk.Label(text="イラつき度(1~10),サプライズ度(1~10),ホラー度(1~10),その時の集中度(1~10)")
    label.place(x=20, y=10)

    button = tk.Button(text="OK")
    button.place(x=150, y=50)

    button["command"] = click

    root.mainloop()


def camera():
    blink_counter = 0
    no_blink_counter = 0
    last_blink_time = time.time()
    playing_sound = False
    play_sound_start_time = 0
    blink_record = []
    camera_start_time = datetime.datetime.now()

    while True:

        ret, rgb = cap.read()
        
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(
            gray, scaleFactor=1.11, minNeighbors=3, minSize=(100, 100)
        )

        if len(faces) == 1:
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

            if len(eyes) <= 1:
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

            if time.time() - last_blink_time > 8:
                if playing_sound is False:
                    print("play sound")
                    # playsound(sound_path, block=False)
                    sound_len = len(sound_path_list)
                    sound_num = random.randint(1,sound_len)
                    sig, sr = sf.read(sound_path_list[sound_num], always_2d=True)
                    sd.play(sig, sr)
                    sd.wait() # sd.playが完了するのを待つ

                    playing_sound = True
                    play_sound_start_time = time.time()
                    blink_record.append([datetime.datetime.now(),"sound"])

                else:
                    if time.time() - play_sound_start_time > 5:
                        playing_sound = False

                no_blink_counter = 0
            blink_record.append([datetime.datetime.now(),len(eyes)])

        cv2.imshow("frame", rgb)
        if cv2.waitKey(1) == 27:
            break  # esc to quit

    with open('./data/'+str(camera_start_time)+'_blinkrecord_sample.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["time","eye_len"])
        for eye_len in blink_record:
            writer.writerow(eye_len)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=2) as executor:
        executor.submit(camera)
        executor.submit(subrepo)


