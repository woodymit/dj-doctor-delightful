import matplotlib.pyplot as plt
import numpy as np

from utils import read_wave
from realtime_cqt import CQT
from realtime_cqt import atom

wave_path = '../test_files/mary_had_a_little_lamb.wav'


def test_read_wave():

    nseconds = 10
    s, sample_rate = read_wave(wave_path, nseconds)
    nseconds_sampled = len(s) / sample_rate
    assert abs(nseconds - nseconds_sampled) < 0.001


def plot_wave_sample():
    nseconds = 10
    s, sample_rate = read_wave(wave_path, nseconds)
    plot_wave(s, sample_rate)


def plot_wave(s, sample_rate):

    t = np.arange(len(s)) * sample_rate

    plt.figure()
    plt.plot(t, s)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Sound Amplitude')
    plt.show()


def plot_atom():
    a = atom(440, 44100, 1000, np.hanning)
    plt.plot(a)
    plt.show()


def plot_atoms():
    fs = 44100
    n_octaves = 5

    cqt = CQT(fs, n_octaves, Q=None, fmin=32.7)
    plt.figure()
    plt.plot(np.real(cqt.atoms.T))
    plt.show()


def plot_X():

    nseconds = 10
    s, sample_rate = read_wave(wave_path, nseconds)

    n_octaves = 5

    cqt = CQT(sample_rate, n_octaves, Q=None, fmin=32.7)

    X = cqt.get_X(s[:cqt.nsample])
    plt.plot(np.real(X))
    plt.show()


def take_cqt(s, sample_rate, cqt_freq, zero_pad=True, 
        fmin=32.7, n_octaves=7, bins_per_octave=12):

    nseconds = len(s) / sample_rate

    cqt = CQT(sample_rate, n_octaves, bins_per_octave=bins_per_octave,
            fmin=fmin)

    if zero_pad:
        s_pad = np.concatenate([
                np.zeros(cqt.nsample // 2 + 1), s,
                np.zeros(cqt.nsample // 2 + 1)])
    else:
        s_pad = s

    n_cqts = int(nseconds * cqt_freq)
    cqt_period = sample_rate / cqt_freq
    nbins = n_octaves * bins_per_octave

    transform = np.zeros((n_cqts, nbins), dtype=complex)
    for i in range(n_cqts):
        t = cqt.transform(s_pad[int(i * cqt_period): int(i * cqt_period + cqt.nsample)])
        transform[i, :] = t

    return transform


def plot_spectrogram(a, **kwargs):
    if 'cmap' in kwargs:
        plt.pcolormesh(a, **kwargs)
    else:
        plt.pcolormesh(a, cmap='magma', **kwargs)
    plt.autoscale(enable=True, axis='both', tight=True)
    plt.tick_params(axis='both', direction='out')


def example_plot_cqt(log_scale=False):

    nseconds = 24
    s, sample_rate = read_wave(wave_path, nseconds)

    cqt_freq = 14  # Hz
    n_octaves = 7
    bins_per_octave = 48
    transform = take_cqt(s, sample_rate, cqt_freq, 
            n_octaves=n_octaves, bins_per_octave=bins_per_octave, zero_pad=True)
    n_cqts = transform.shape[0]
    nseconds_cqt = n_cqts / cqt_freq

    transform = np.abs(transform)
    if log_scale:
        log_padding = 0.001
        transform = np.log(transform + log_padding)

    bottom_percentile = 2
    top_percentile = 100
    vmin = np.percentile(transform, bottom_percentile)
    vmax = np.percentile(transform, top_percentile)
    plot_spectrogram(transform.T, vmin=vmin, vmax=vmax)

    print(
        'min:', transform.min(),
        '\ntvmin:', vmin,
        '\nvmax:', vmax,
        '\nmax:', transform.max())

    x_ticks = range(0, n_cqts, cqt_freq)
    x_labels = range(int(nseconds_cqt))

    y_ticks = np.arange(n_octaves) * bins_per_octave
    y_labels = ['C' + str(i + 1) for i in range(n_octaves)]

    plt.xticks(x_ticks, x_labels)
    plt.yticks(y_ticks, y_labels)

    plt.show() 


if __name__ == '__main__':

    # # Plot the real part of CQT atoms
    # plot_atoms()

    # # Plot the downsampled matrix created for the CQT
    # plot_X()

    # Plot CQT for mary had a little lamb
    example_plot_cqt()
