import sys
import time

import settings
import utils

import numpy as np
from PyQt4 import QtGui


class ToolStack(object):

    hang_time = 1
    freq_staleness_buffer_len = 20

    def __init__(self, sampler, vis_alg):
        self.sampler = sampler
        self.vis_alg = vis_alg

        # Begin sampling
        self.sampler.stream_start()
        self.hang_till_sampler_starts()
        self.freq_staleness = 0
        self.prev_freq = None
        self.freq_staleness_buffer = utils.CircularBuffer(
                self.freq_staleness_buffer_len, np.uint16)

    def hang_till_sampler_starts(self):
        i = 0
        while (self.sampler.data is None or self.sampler.fft is None):
            print('i:{0}'.format(i))
            time.sleep(self.hang_time)

    def get_hex_arr(self):

        self.sampler.stream_readchunk_sequential()

        assert (self.sampler.data is not None and self.sampler.fft is not None)
        freq = self.sampler.fft[:500]

        if self.prev_freq is not None:
            is_stale = np.array_equal(freq, self.prev_freq)
            if is_stale:
                self.freq_staleness += 1
            else:
                self.freq_staleness_buffer.write(self.freq_staleness)
                self.freq_staleness = 0
        self.prev_freq = freq

        hex_arr = self.vis_alg.freq_to_hex(freq)
        return hex_arr, np.mean(self.freq_staleness_buffer.tape)


    def close(self):
        self.sampler.close()


class FullStack(object):

    def __init__(self, sampler_class, vis_alg_class, light_sim_class):

        self.sampler_class = sampler_class
        self.vis_alg_class = vis_alg_class
        self.light_sim_class = light_sim_class


    def start(self):

        app = QtGui.QApplication(sys.argv)

        self.light_sim = self.light_sim_class()

        rate = 44100 * 2
        self.sampler = self.sampler_class(settings.STEREO_MONITOR_SOURCE, rate)
        self.vis_alg = self.vis_alg_class(self.light_sim.nlights)
        self.tool_stack = ToolStack(
                self.sampler,
                self.vis_alg)

        self.light_sim.get_hex_arr = self.tool_stack.get_hex_arr

        self.light_sim.update()

        app.exec_()

    def close(self):
        self.tool_stack.close()
