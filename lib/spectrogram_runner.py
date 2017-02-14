from renderers.pyqt.spectrogram_widget import SpectrogramWidget
from samplers.pyaudio_sampler import PyAudioSampler
from spectrum_analyzers.spectrum_analyzers import WindowedSTFT

from PyQt4 import QtGui


if __name__ == '__main__':
    
    # Sampler params
    pa_device_index = None
    sample_rate = 44100 * 2

    # Instantiate sampler and spectrum analyzer
    sampler = PyAudioSampler(pa_device_index, sample_rate)
    spectrum_analyzer = WindowedSTFT(sampler.nsamples, sampler.rate)

    app = QtGui.QApplication([])
    spectrogram_widget = SpectrogramWidget(spectrum_analyzer)

    # Add spectrum getter function to the widget
    def get_spectrum():
        return spectrum_analyzer.get_spectrum(sampler.read_chunk())
    spectrogram_widget.get_spectrum = get_spectrum

    # Starts QtTimer.singleShot update loop
    spectrogram_widget.update()

    # Start the app
    print('Entering blocking PyQt4 GUI')
    app.exec_()
    print('Exiting blocking PyQt4 GUI')
