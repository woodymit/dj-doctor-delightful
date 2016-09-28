import factory
from pyqt.light_sim import QTLightSim
from samplers import SWHear
from vis_algs import bass_flash
from vis_algs import bin_fft
from vis_algs import bin_fft_v2
from vis_algs import smooth_visualizer_abc
from vis_algs import rainbow_equalizer


if __name__ == '__main__':
    app = factory.FullStack(
            SWHear.SWHear, 			# Audio sampler (Threaded)
            smooth_visualizer_abc.Visualizer, 	# Visualization Algorithm
            QTLightSim) 			# Lights
    app.start()
