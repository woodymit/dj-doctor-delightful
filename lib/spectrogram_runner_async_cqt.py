from renderers.pyqt.spectrogram_widget_basic import SpectrogramWidget
from samplers.pyaudio_sampler_async import PyAudioSamplerAsync
from spectrum_analyzers.spectrum_analyzers import CQT

from PyQt4 import QtGui


if __name__ == '__main__':
    
    # Sampler params
    pa_device_index = None
    # sample_rate = 44100 * 2
    sample_rate = 22050
    nsamples = 4096 // 8
    max_freq = 2000
    nchunks = 1

    n_octaves = 7
    bins_per_octave = 12
    n_bins = n_octaves * bins_per_octave
    n_frames = 250


    # Instantiate sampler and spectrum analyzer
    sampler = PyAudioSamplerAsync(pa_device_index, sample_rate, nsamples,
            nchunks)
    spectrum_analyzer = CQT(sampler.nsamples * nchunks, sampler.rate, n_octaves)

    app = QtGui.QApplication([])
    spectrogram_widget = SpectrogramWidget((n_frames, n_bins))

    sampler.signal = spectrogram_widget.read_collected

    # Add spectrum getter function to the widget
    spectrogram_widget.get_spectrum = spectrum_analyzer.get_spectrum

    sampler.start()

    # Start the app
    print('Entering blocking PyQt4 GUI')
    app.exec_()
    print('Exiting blocking PyQt4 GUI')
