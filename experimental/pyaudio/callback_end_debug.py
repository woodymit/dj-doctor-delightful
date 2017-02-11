"""PyAudio Example: Play a wave file (callback version)."""
import time

import numpy as np
import pyaudio

p = pyaudio.PyAudio()
x = []
stop = False
i = 0


def callback(in_data, frame_count, time_info, status):
    global stop
    # print('in_data[0]:{0}'.format(in_data[0]))
    # print('frame_count:{0}\n'.format(frame_count))
    global i
    print('i:', i)
    i += 1
    x.append(np.mean(list(in_data)))

    if stop:
        print('stopping!')
        return (None, pyaudio.paComplete)

    return (None, pyaudio.paContinue)


stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                # input_device_index=0,
                stream_callback=callback)

stream.start_stream()

time.sleep(1)
# print('x:\n', '\t\n'.join(map(str, x)))
print('done printing x')

stop = True
print('stop=True')
time.sleep(1)
print('stop=True + 1s')

# stop stream
stream.stop_stream()
print('stopped\n')
stream.close()
print('closed\n')

# close PyAudio
p.terminate()
print('terminated\n')
