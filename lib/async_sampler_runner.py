import wave

from samplers.pyaudio_sampler_async import PyAudioSamplerAsync

import numpy as np
from PyQt4 import QtGui

WAVE_OUTPUT_FILENAME = 'test_circular_buffer_recording.wav'
CHANNELS = 1

if __name__ == '__main__':
    
    # Sampler params
    pa_device_index = None
    sample_rate = 44100 * 2
    nsamples = 4096 * 2
    max_freq = 2000

    # Instantiate sampler and spectrum analyzer
    sampler = PyAudioSamplerAsync(pa_device_index, sample_rate, nsamples)

    prev_i = -1
    record_length = 10 # seconds
    record_nsamples = record_length * sample_rate
    recorded_data = np.zeros(record_nsamples, dtype=sampler.buffer.tape.dtype)
    buffer_len = sampler.buffer.n * sampler.buffer.chunk
    nwrites = record_nsamples // buffer_len
    i = 0
    while(i < nwrites):
        buffer_idx = sampler.buffer.i
        if buffer_idx != prev_i:
            prev_i = buffer_idx
            print('new chunk:{0}'.format(buffer_idx))

            if buffer_idx == 4:
                print('recording')
                recorded_data[i * buffer_len:(i+1) * buffer_len] = sampler.buffer.unwind()
                i += 1

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(recorded_data.dtype.itemsize)
    waveFile.setframerate(sample_rate)
    waveFile.writeframes(recorded_data.tobytes())
    waveFile.close()
