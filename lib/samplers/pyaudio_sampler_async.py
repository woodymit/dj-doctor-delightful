from samplers.sampler_base import SamplerABC
from utils import CircularChunkBuffer

import pyaudio
import time
import numpy as np

MONITOR_PATTERN = 'monitor'


class PyAudioSamplerAsync(SamplerABC):

    def __init__(self, device=None, rate=44100, nsamples=4096, nchunks=5):
        self.buffer = CircularChunkBuffer(nchunks, nsamples, np.int16)
        self.device = device
        self.nsamples = nsamples  # number of data points to read at a time
        self.rate = rate

        self.p = pyaudio.PyAudio()
        self.initiate()
        self.start()

    def max_fps(self):
        return self.rate / self.nsamples

    # DEVICE TESTS

    def valid_low_rate(self, device):
        """set the rate to the lowest supported audio rate."""
        for testrate in [44100]:
            if self.valid_test(device, testrate):
                return testrate
        print("SOMETHING'S WRONG! I can't figure out how to use DEV", device)
        return None

    def valid_test(self, device, rate=44100):
        """given a device ID and a rate, return TRUE/False if it's valid."""
        print('Testing device: {0} at sampling rate: {1}'.format(device, rate))
        try:
            self.info = self.p.get_device_info_by_index(device)
            if not self.info["maxInputChannels"] > 0:
                print("Test Failed\n")
                return False
            stream = self.p.open(format=pyaudio.paInt16, channels=2,
                    input_device_index=device, frames_per_buffer=self.nsamples,
                    rate=int(self.info["defaultSampleRate"]), input=True)
            stream.close()
            print("Test Passed\n")
            return True
        except:
            print("Test Failed\n")
            return False

    def valid_input_devices(self):
        """
        See which devices can be opened for input.
        call this when no PyAudio object is loaded.
        """
        inputs = []
        for device in range(self.p.get_device_count()):
            if self.valid_test(device):
                inputs.append(device)
        if len(inputs) == 0:
            print("No valid input devices found!")
        else:
            print("Found %d valid input devices: %s" % (len(inputs), inputs))
        return inputs

    def find_output_monitor_device(self):
        print('Searching for output monitor device:')

        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        monitor_index = None
        for i in range(numdevices):

            device_info = self.p.get_device_info_by_host_api_device_index(0, i)
            max_input_channels = device_info.get('maxInputChannels')
            name = device_info.get('name')
            if max_input_channels > 0:
                print(
                    '\tInput Device index:', i,
                    '\tMax Input Channels:', max_input_channels,
                    '\tName:', name)

                if MONITOR_PATTERN in name:
                    monitor_index = i
        return monitor_index

    # SETUP AND SHUTDOWN

    def initiate(self):
        """run this after changing settings (like rate) before recording"""

        if self.device is None:
            # First try to find an output monitor
            self.device = self.find_output_monitor_device()
        if self.device is None:
            # Second pick the first valid input device
            self.device = self.valid_input_devices()[0]
        if self.rate is None:
            self.rate = self.valid_low_rate(self.device)
        if not self.valid_test(self.device, self.rate):
            print('Guessing a valid microphone device/rate...')
            self.device = self.valid_input_devices()[0]
            self.rate = self.valid_low_rate(self.device)
        
        msg = 'Using device: {0}\n'.format(self.device)
        msg += 'Recording from "%s" ' % self.info["name"]
        msg += '(device %d) ' % self.device
        msg += 'at %d Hz' % self.rate
        msg += '\bMax FPS: {0}  at [sample rate:{1}Hz   chunk size:{2}]'.format(
                self.max_fps(), self.rate, self.nsamples)
        print(msg)

    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.stream.stop_stream()
        self.p.terminate()

    # STREAM HANDLING
    def read_chunk(self):
        pass

    def read(self):
        return self.buffer.unwind()

    def stream_callback(self, in_data, frame_count, time_info, status_flags):

        self.buffer.write(np.fromstring(in_data, 'int16'))
        return (None, pyaudio.paContinue)

    def start(self):

        print(' -- Starting stream -- ')
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1,
                rate=self.rate, input=True, frames_per_buffer=self.nsamples,
                input_device_index=self.device, stream_callback=self.stream_callback)
