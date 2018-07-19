import subprocess
import time
from matplotlib import pyplot as plt
from threading import Thread
from queue import Queue, Empty
from pydub import AudioSegment
import io

FRAMERATE = 10000


def main():
    play_wave_nonblocking()


def play_wave_nonblocking():
    def enqueue_output(out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    cmd = f"parec -d  alsa_output.pci-0000_00_1b.0.analog-stereo.monitor --channels 1 --rate {FRAMERATE}|sox -t raw -r {FRAMERATE} -b 16 -e signed -c 1 -r {FRAMERATE} - -t wav -V0 -"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    q = Queue()
    t = Thread(target=enqueue_output, args=(ps.stdout, q))
    t.daemon = True
    t.start()


    start_frame = time.time()
    buffer = bytearray()
    empty = False
    last_operation = time.time()
    first = True
    header = None
    while time.time() - start_frame < 1000:
        try:
            line = q.get_nowait()  # or q.get(timeout=.1)
        except Empty:
            if not empty:
                empty = True
                empty_time = time.time()
            elif time.time() - empty_time > 1.5:
                print(0)
        else:
            if first:
                header = line[:46]
                first = False
                continue
            print(1)
            empty = False
            buffer += line

        if time.time() - last_operation > 5:
            # EXPERIMENTS
            if not buffer:
                last_operation = time.time()
                continue

            iob = io.BytesIO(header + buffer)
            sound = AudioSegment.from_file(iob, format="wav", channels=1, sample_width=2, frame_rate=FRAMERATE)

            num_chunks = 400  # px
            chunk_size = int(len(sound) / num_chunks)

            loudness_over_time = []
            for i in range(0, len(sound), chunk_size):
                chunk = sound[i:i + chunk_size]
                loudness_over_time.append(chunk.rms)
            plt.plot(loudness_over_time)
            plt.show()

            buffer = bytearray()
            last_operation = time.time()


if __name__ == '__main__':
    main()

    # wavef = wave.open('sound.wav', 'w')
    # wavef.setnchannels(1)
    # wavef.setsampwidth(2)
    # wavef.setframerate(FRAMERATE)
    # frame = np.frombuffer(buff, np.uint16)
    # wavef.writeframesraw(line)