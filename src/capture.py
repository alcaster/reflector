import string
import subprocess
import time
from threading import Thread
from queue import Queue, Empty
import io
import logging
from multiprocessing import Process, cpu_count, Queue as QueueMulti

from pydub import AudioSegment

FRAMERATE = 41000

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Capturer:
    def __init__(self, cmd):
        self.playing = True
        self.last_operation = time.time()
        self.cmd = cmd
        self.last_playing_update = None
        self.start_wave_nonblocking = None
        self.sound_interval = .7
        self.event_interval = 1

        self.queue = QueueMulti()

    def play_wave2(self):
        consumer = Process(target=self.consume, args=(self.queue,))
        consumer.start()
        producer = Process(target=self.produce, args=(self.queue,))
        producer.start()

    def produce(self, queue):
        idx = 0
        start_time = time.time()
        last_operation = time.time()
        produce_interval = 0.2
        while True:
            if time.time() - last_operation > produce_interval:
                print("putting")
                queue.put(string.ascii_letters[idx])
                idx+=1
                last_operation = time.time()

    def consume(self, queue):
        start_time = time.time()
        last_operation = time.time()
        while True:
            if time.time() - last_operation > self.event_interval:
                current = []
                while True:
                    try:
                        current.append(queue.get(False))
                    except Empty:
                        break
                print(current)
                last_operation = time.time()

    def play_wave_nonblocking(self):  # todo collecting and adding to buffer should be in separate thread
        first_skip = 1

        ps = subprocess.Popen(self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        q = Queue()
        t = Thread(target=self.enqueue_output, args=(ps.stdout, q))
        t.daemon = True
        t.start()

        buffer = bytearray()
        self.start_wave_nonblocking = time.time()
        not_play_start = self.start_wave_nonblocking
        temporal_playing = False

        current_value = 0
        counter = 0
        while time.time() - self.start_wave_nonblocking < 10:
            try:
                line = q.get_nowait()  # or q.get(timeout=.1)
            except Empty:
                if temporal_playing:
                    not_play_start = time.time()
                    temporal_playing = False
            else:
                temporal_playing = True
                buffer += line

            if time.time() - self.start_wave_nonblocking < first_skip:  # skip first n seconds, sometimes first second is empty
                continue

            if self.last_playing_update and time.time() - self.last_playing_update > self.sound_interval:  # update self.playing
                self.set_is_playing(not_play_start, temporal_playing, first=False)

            if time.time() - self.last_operation > self.event_interval:
                if self.last_playing_update is None:  # if there is event and interval is shorter than update interval for self.playing
                    self.set_is_playing(not_play_start, temporal_playing, first=True)
                self.last_operation = time.time()

                loudness_over_time = []
                if buffer:
                    iob = io.BytesIO(buffer)
                    sound = AudioSegment.from_file(iob, format="raw", channels=1, sample_width=2, frame_rate=FRAMERATE)

                    num_chunks = 1  # px
                    chunk_size = int(len(sound) / num_chunks)
                    if chunk_size > 0:
                        for i in range(0, len(sound), chunk_size):
                            chunk = sound[i:i + chunk_size]
                            try:
                                loudness_over_time.append(
                                    chunk.rms)  # im not sure by what len(chunk) has to be divisible so there is double try
                            except Exception:
                                try:
                                    loudness_over_time.append(chunk[:-1].rms)
                                except Exception:
                                    print("Cannot calculate rms.")
                    if loudness_over_time:
                        current_value = loudness_over_time[0]
                        counter += 1

                if not self.playing:
                    current_value = 0

                logger.info(current_value)
                buffer = bytearray()
        logger.info(counter)

    def set_is_playing(self, not_play_start, temporal_playing, first=False):  # handle first, if first is not playing
        if temporal_playing:
            self.playing = True
        else:
            if first:
                self.playing = False if not_play_start == self.start_wave_nonblocking else True
            else:
                self.playing = False if time.time() - not_play_start > self.sound_interval else True
        self.last_playing_update = time.time()

    @staticmethod
    def enqueue_output(out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()


def main():
    cmd = f"parec -d alsa_output.pci-0000_00_1b.0.analog-stereo.monitor --channels 1 --rate {FRAMERATE}"
    capturer = Capturer(cmd)
    capturer.play_wave2()


if __name__ == '__main__':
    main()

    # wavef = wave.open('sound.wav', 'w')
    # wavef.setnchannels(1)
    # wavef.setsampwidth(2)
    # wavef.setframerate(FRAMERATE)
    # frame = np.frombuffer(buff, np.uint16)
    # wavef.writeframesraw(line)
