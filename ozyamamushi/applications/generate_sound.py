import numpy as np
from scipy.io.wavfile import write

if __name__ == "__main__":
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
        return write("./python-sound-test.wav", rate=rate, data=music)

    mml_twinkle_star = "CCGGAAGRFFEEDDCR"
    play_mml(mml_twinkle_star)
