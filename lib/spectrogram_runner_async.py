from renderers.pyqt.spectrogram_widget_async import SpectrogramWidget
from samplers.pyaudio_sampler_async import PyAudioSamplerAsync
from spectrum_analyzers.spectrum_analyzers import WindowedSTFT

from PyQt4 import QtGui


if __name__ == '__main__':
    
    # Sampler params
    pa_device_index = None
    sample_rate = 44100 * 2
    nsamples = 4096
    max_freq = 2000
    nchunks = 5


    # Instantiate sampler and spectrum analyzer
    sampler = PyAudioSamplerAsync(pa_device_index, sample_rate, nsamples,
            nchunks)
    spectrum_analyzer = WindowedSTFT(sampler.nsamples * nchunks, sampler.rate,
            logscale=True)

    app = QtGui.QApplication([])
    spectrogram_widget = SpectrogramWidget(spectrum_analyzer, max_freq)
    spectrogram_widget.read_collected.connect(spectrogram_widget.update)

    sampler.signal = spectrogram_widget.read_collected

    # Add spectrum getter function to the widget
    spectrogram_widget.get_spectrum = spectrum_analyzer.get_spectrum

    sampler.start()

    # Start the app
    print('Entering blocking PyQt4 GUI')
    app.exec_()
    print('Exiting blocking PyQt4 GUI')
