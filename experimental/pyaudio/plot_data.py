import pickle

import matplotlib.pyplot as plt
import numpy as np

pickle_path = 'samples_1.pickle'


with open(pickle_path, 'rb') as fh:
    samples = pickle.load(fh)

n, m = samples.shape

print(samples)
print('sample shape:', samples.shape)
print('# nonzero:', np.count_nonzero(samples))
print('max:', np.max(samples))


# X = np.arange(m)
# Y = samples[20]

X = np.tile(np.arange(m), (n, 1))
offset = np.tile(np.arange(n).reshape(n, 1), (1, m)) * 256
print('offset:', offset)
Y = samples + offset

n_idxs = [20, 21, 22]
n_idxs = np.arange(100)

print('X:', X[n_idxs])
print('Y:', Y[n_idxs])

plt.close()
print('X[n_idxs].shape:', X[n_idxs].shape)
plt.plot(X[n_idxs].T, Y[n_idxs].T)
plt.xlim(0, m)
# plt.plot(X[20], Y[20], X[21], Y[21])
plt.show()
