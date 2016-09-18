import sys
import time

import settings

from PyQt4 import QtGui, QtCore


class ToolStack(object):

    hang_time = 1

    def __init__(self, sampler, vis_alg):
        self.sampler = sampler
        self.vis_alg = vis_alg

        # Begin sampling
        self.sampler.stream_start()
        self.hang_till_sampler_starts()

    def hang_till_sampler_starts(self):
        i = 0
        while (self.sampler.data is not None or self.sampler.fft is not None):
            print('i:{0}'.format(i))
            time.sleep(self.hang_time)

    def get_hex_arr(self):
        assert (self.sampler.data is not None and self.sampler.fft is not None)
        rgb_arr = self.vis_alg.freq_to_hex(self.sampler.fft[:500])
        return rgb_arr

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

        self.sampler = self.sampler_class(settings.STEREO_MONITOR_SOURCE)
        self.vis_alg = self.vis_alg_class(self.light_sim.nlights)
        self.tool_stack = ToolStack(
                self.sampler,
                self.vis_alg)

        self.light_sim.get_hex_arr = self.tool_stack.get_hex_arr

        self.light_sim.show()
        self.light_sim.update()  # start with something

        app.exec_()

    def close(self):
        self.tool_stack.close()
