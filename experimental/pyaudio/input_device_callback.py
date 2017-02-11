"""PyAudio Example: Play a wave file (callback version)."""
import pickle
import time

import numpy as np
import pyaudio

p = pyaudio.PyAudio()
x = []
alldata = np.zeros((100, 2048))
stop = False
i = 0


def callback(in_data, frame_count, time_info, status):
    global stop
    global i
    global alldata
    print('i:', i)
    i += 1
    x.append(np.mean(list(in_data)))
    alldata[i - 1, :] = np.array(list(in_data))

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
print('x:\n', '\t\n'.join(map(str, x)))
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

with open('output_1.txt', 'w') as fh:
    for row in alldata:
        fh.write('\t'.join(map(str, row)) + '\n')


def subseq_indices(subseq, seq):
    subseq = list(subseq)
    seq = list(seq)
    return [x for x in range(len(seq)) if seq[x:x + len(subseq)] == subseq]


with open('samples_1.pickle', 'wb') as fh:
    pickle.dump(alldata, fh)

sample_20 = alldata[20]
sample_21 = alldata[21]

print('idxs:', subseq_indices(sample_20[:10], sample_21))

# import ipdb
# ipdb.set_trace()
