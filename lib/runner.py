import factory
from pyqt.light_sim import QTLightSim
from samplers import SWHear
from vis_algs import bass_flash
from vis_algs import bin_fft
from vis_algs import rainbow_equalizer


if __name__ == '__main__':
    app = factory.FullStack(SWHear.SWHear, bass_flash.Visualizer, QTLightSim)
    app.start()
