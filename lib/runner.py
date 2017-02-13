from factory_sequential import ToolStack
from renderers.pyqt.light_sim import QTLightSim
from renderers.teensy.light_sender import LightSender
from samplers.pyaudio_sampler import PyAudioSampler
from spectrum_analyzers.spectrum_analyzers import WindowedSTFT
from vis_algs.smooth_visualizer import Visualizer


if __name__ == '__main__':
    app = ToolStack(
            PyAudioSampler,                     # Audio sampler
            WindowedSTFT,						# Spectrum analyzer
            Visualizer,   						# Visualization algorithm
            QTLightSim)                         # Light simulator / Light serial sender
    app.start()
