import numpy as np
import subprocess
import wave
import time
from matplotlib import pyplot as plt


def main():
    play_wave()


def play_wave():
    cmd = "parec -d  alsa_output.pci-0000_00_1b.0.analog-stereo.monitor --channels 1 --rate 88200|sox -t raw -r 88200 -b 16 -e signed -c 1 -r 44100 - -t wav -"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    buff = bytearray()
    wavef = wave.open('sound.wav', 'w')
    wavef.setnchannels(2)
    wavef.setsampwidth(2)
    wavef.setframerate(44100)

    start = time.time()
    while time.time() - start < 2:
        line = ps.stdout.readline()
        if line:
            wavef.writeframesraw(line)
            buff = buff + line
    frame = np.frombuffer(buff, np.uint16)
    plt.plot(frame[:800])
    plt.show()


if __name__ == '__main__':
    main()
