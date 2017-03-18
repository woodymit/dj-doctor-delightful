import numpy as np


def shorkhuber_optimal_N(fs, fk, bins_per_octave=12, q=1):
	return int(np.round(q * fs / (fk * (2 ** (1/bins_per_octave) - 1))))


def get_N(fk, fs, Q):
	return Q * fs / fk


def atom(fk, fs, nk, window):
	return 1 / nk * window(nk) * np.exp(-1j * 2 * np.pi * fk / fs * np.arange(nk))


def downsampled(signal_array, factor):
	return signal_array[::factor]


def cut_from_center(signal_array, center, n):
	cut_start = center - n // 2
	cut_end = center + (n - n // 2)
	assert cut_start >= 0
	assert cut_end <= len(signal_array)
	return signal_array[cut_start:cut_end]


class CQT(object):
	'''This implementation is loosely based on the recursive sub-sampling method
    described by [1], but for realtime CQT computation.

    [1] Schoerkhuber, Christian, and Anssi Klapuri.
        "Constant-Q transform toolbox for music processing."
        7th Sound and Music Computing Conference, Barcelona, Spain. 2010.
    '''


	def __init__(self, fs, n_octaves, bins_per_octave=12, fmin=32.7,
			window=np.hanning):
		self.fs = fs
		self.n_octaves = n_octaves
		self.bins_per_octave = bins_per_octave
		self.fmin = fmin
		self.window = window

		self.top_octave_fmin = self.fmin * 2 ** (self.n_octaves - 1)
		self.nmax = shorkhuber_optimal_N(self.fs, self.top_octave_fmin,
				self.bins_per_octave)

		self.nsample = self.nmax * 2 ** (self.n_octaves - 1)

		self.atoms = self.get_top_octave_atoms()

	def get_top_octave_atoms(self):
		atoms = np.zeros((self.bins_per_octave, self.nmax), dtype=complex)
		atom_center = self.nmax // 2

		for b in range(self.bins_per_octave):
			fk = self.top_octave_fmin * 2 ** (b / self.bins_per_octave)
			nk = shorkhuber_optimal_N(self.fs, fk, self.bins_per_octave)
			atom_start = atom_center - nk // 2
			atom_end = atom_center + (nk - nk // 2)
			atoms[b, atom_start:atom_end] = atom(fk, self.fs, nk, self.window)

		return atoms

	def get_X(self, chunk):
		assert len(chunk) == self.nsample
		X = np.zeros((self.nmax, self.n_octaves))

		nsample = self.nsample

		for o in range(self.n_octaves):
			X[:, o] = cut_from_center(downsampled(chunk, 2 ** o), nsample // 2, self.nmax)
			nsample //= 2
		return X

	def transform(self, chunk):
		X = self.get_X(chunk)
		transform = np.matmul(self.atoms, X)
		return transform.T.flatten()
