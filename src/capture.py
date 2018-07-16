import asyncio
import subprocess
import sys

from matplotlib import pyplot as plt
import numpy as np
import pyaudio
from scipy.io.wavfile import write

from fifo import FifoFileBuffer

CHUNKSIZE = 10000

pya = pyaudio.PyAudio()
stream = pya.open(format=pyaudio.get_format_from_width(2), channels=2, rate=44100, input=True, output=True)


async def producer():
    # cmd = "parec -d  alsa_output.pci-0000_00_1b.0.analog-stereo.monitor --channels 1 --rate 44100| lame -r -V0 -"
    cmd = "parec -d  alsa_output.pci-0000_00_1b.0.analog-stereo.monitor --channels 2 --rate 44100| sox -t raw -b 16 -e signed -c 2 -v 7 -r 44100 - -t wav"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = ps.stdout.readline()
        await stream.write(line)


async def consumer():
    i = 0
    np_data = np.array([],dtype=np.int16)
    while True:
        data = stream.read(CHUNKSIZE, exception_on_overflow=False)
        i += 1
        print("writting")
        print(data)
        new_data = np.fromstring(data, dtype=np.int16)
        print(new_data.shape)
        print(np_data.shape)
        np_data = np.concatenate((new_data,np_data))
        if np_data.shape[0] > 100000:
            write('test.wav', 44100, np_data)
            sys.exit(0)
        print("written")


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(producer())
    loop.create_task(consumer())
    loop.run_forever()


if __name__ == '__main__':
    main()

    # wf = wave.open(wav_file, 'rb')
    #
    # sample_width=wf.getsampwidth()
    # channels=wf.getnchannels()
    # rate=wf.getframerate()
    # second=sample_width*channels*rate
    #
    # def callback(in_data, frame_count, time_info, status):
    #     data = wf.readframes(frame_count)
    #     return (data, pyaudio.paContinue)
    #
    # p = pyaudio.PyAudio()
    #
    # stream = p.open(format=p.get_format_from_width(sample_width),
    #             channels=channels,
    #             rate=int(rate),
    #             output=True,
    #             stream_callback=callback)
    # stream.start_stream()
    #
    # while stream.is_active():
    #     time.sleep(0.1)
