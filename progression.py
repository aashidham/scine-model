class Linear(object):

    def __init__(self, low, high, n_samples):
        assert high > low
        self._low = float(low)
        self._high = float(high)
        assert (type(n_samples) == int) and (n_samples > 1)
        self._n_samples = n_samples
        self._i = 0

    def __iter__(self):
        return self

    def next(self):
        if self._i < self._n_samples:
            v = (self._i * (self._high - self._low) / (self._n_samples - 1)) + self._low
            self._i += 1
            return v
        else:
            raise StopIteration()
