"""
this is a stripped down version of the SWHear class.
It's designed to hold only a single audio sample in memory.
check my githib for a more complete version:
    http://github.com/swharden
"""

import pyaudio
import time
import numpy as np
import threading

MONITOR_PATTERN = 'monitor'


def getFFT(data, rate):
    """Given some data and rate, returns FFTfreq and FFT (half)."""
    data = data * np.hamming(len(data))
    fft = np.fft.fft(data)
    fft = np.abs(fft)
    # fft=10*np.log10(fft)
    freq = np.fft.fftfreq(len(fft), 1.0 / rate)
    return freq[:int(len(freq) / 2)], fft[:int(len(fft) / 2)]


class SWHear(object):
    """
    The SWHear class is made to provide access to continuously recorded
    (and mathematically processed) microphone data.
    """

    def __init__(self, device=None, rate=None):
        """fire up the SWHear class."""
        self.p = pyaudio.PyAudio()
        # self.chunk = 4096  # number of data points to read at a time
        self.chunk = 1024  # number of data points to read at a time
        self.device = device
        self.rate = rate

    # SYSTEM TESTS

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
                return False
            stream = self.p.open(format=pyaudio.paInt16, channels=2,
                    input_device_index=device, frames_per_buffer=self.chunk,
                    rate=int(self.info["defaultSampleRate"]), input=True)
            stream.close()
            print("Test Passed\n")
            return True
        except:
            return False

    def valid_input_devices(self):
        """
        See which devices can be opened for microphone input.
        call this when no PyAudio object is loaded.
        """
        mics = []
        for device in range(self.p.get_device_count()):
            if self.valid_test(device):
                mics.append(device)
        if len(mics) == 0:
            print("no microphone devices found!")
        else:
            print("found %d microphone devices: %s" % (len(mics), mics))
        return mics

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
            self.device = self.find_output_monitor_device()
        if self.device is None:
            self.device = self.valid_input_devices()[0]  # pick the first one
        if self.rate is None:
            self.rate = self.valid_low_rate(self.device)
        if not self.valid_test(self.device, self.rate):
            print('Guessing a valid microphone device/rate...')
            self.device = self.valid_input_devices()[0]  # pick the first valid device
            self.rate = self.valid_low_rate(self.device)
            print('Using device: {0}'.format(self.device))
        self.datax = np.arange(self.chunk) / float(self.rate)
        msg = 'Recording from "%s" ' % self.info["name"]
        msg += '(device %d) ' % self.device
        msg += 'at %d Hz' % self.rate
        print(msg)

    def close(self):
        """gently detach from things."""
        print(" -- sending stream termination command...")
        self.keepRecording = False  # the threads should self-close
        while(self.t.isAlive()):  # wait for all threads to close
            time.sleep(.1)
        self.stream.stop_stream()
        self.p.terminate()

    # STREAM HANDLING

    def stream_readchunk_sequential(self):
        self.data = np.fromstring(
                self.stream.read(self.chunk), dtype=np.int16)
        self.fftx, self.fft = getFFT(self.data, self.rate)

    def stream_readchunk(self):
        """reads some audio and re-launches itself"""
        try:
            self.data = np.fromstring(
                self.stream.read(self.chunk), dtype=np.int16)
            self.fftx, self.fft = getFFT(self.data, self.rate)

        except Exception as E:
            print(" -- exception! terminating...")
            print(E, "\n" * 5)
            self.keepRecording = False
        if self.keepRecording:
            self.stream_thread_new()
        else:
            self.stream.close()
            self.p.terminate()
            print(" -- stream STOPPED")

    def stream_thread_new(self):
        self.t = threading.Thread(target=self.stream_readchunk)
        self.t.start()

    def stream_start(self):
        """adds data to self.data until termination signal"""
        self.initiate()
        print(" -- starting stream")
        self.keepRecording = True  # set to False later to terminate stream
        self.data = None  # will fill up with threaded recording data
        self.fft = None
        self.dataFiltered = None  # same
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1,
                rate=self.rate, input=True, frames_per_buffer=self.chunk)
        self.stream_readchunk_sequential()


if __name__ == "__main__":
    ear = SWHear()
    ear.stream_start()  # goes forever
    while True:
        print(ear.data)
        time.sleep(.1)
    print("DONE")
