import numpy as np


def get_gaussian(mu, sig):
    def P(x):
        return (2 * sig ** 2 * np.pi) ** -0.5 * np.exp(
                -(x - mu) ** 2 / (2 * sig ** 2))
    return P


def gaussian_smooth(series, lim, n, sig):

    max_d = int(3 * sig)
    gauss = get_gaussian(0, sig)
    gauss_arr = gauss(np.arange(-max_d, max_d + 1))

    # Pad input array if convolutions would fall outside its range
    lpad = max(max_d - lim[0], 0)
    rpad = max(max_d - (len(series) - lim[1]), 0)
    if lpad and rpad:
        myseries = np.hstack((np.zeros(lpad), series, np.zeros(rpad)))
    elif lpad:
        myseries = np.hstack((series, np.zeros(rpad)))
    elif rpad:
        myseries = np.hstack((series, np.zeros(rpad)))
    else:
        myseries = series

    out = np.zeros(n) - 1
    for light_i, fft_i in enumerate(np.linspace(lim[0], lim[1] - 1, n)):
        xmin = int(fft_i + lpad - max_d)
        xmax = int(fft_i + lpad + max_d + 1)
        conv = gauss_arr.dot(myseries[xmin:xmax])
        out[light_i] = conv

    assert np.amin(out) >= 0
    return out
