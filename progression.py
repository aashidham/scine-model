import math


class Constant(object):

    def __init__(self, constant):
        self._c = constant

    def __iter__(self):
        return self

    def next(self):
        if self._c is None:
            raise StopIteration()
        else:
            c = self._c
            self._c = None
            return c


class Linear(object):

    def __init__(self, low, high, n_samples):
        assert high > low, '%s <= %s' % (high, low)
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


class Logarithmic(Linear):

    def next(self):
        if self._i <= self._n_samples:
            v = 10.0 ** (math.log(self._low, 10) + ((math.log(self._high, 10) - math.log(self._low, 10)) * self._i / float(self._n_samples)))
            self._i += 1
            return v
        else:
            raise StopIteration()
