import numpy as np


class Sample(object):
    _m = None
    _s = None
    _s0 = None
    _n = None
    _data = None
    _name = None

    def __init__(self, name="A sample"):
        self._name = name

    @staticmethod
    def from_data(name, data):
        result = Sample(name)
        result._data = data
        return result

    @staticmethod
    def from_params(name, n, m, s, s0):
        result = Sample(name)
        result._m = m
        result._s = s
        result._s0 = s0
        result._n = n

    @staticmethod
    def from_distribution(name, dist, count):
        data = dist.rvs(size=count)
        return Sample.from_data(name, data)

    def data(self):
        if self._data is None:
            raise ValueError("No data is provided for this sample")
        return self._data

    def n(self):
        if self._n is None:
            self._n = len(self.data())
        return self._n

    def mean(self):
        if self._m is None:
            self._m = np.mean(self.data())
        return self._m

    def s(self):
        if self._s is None:
            self._s = np.std(self.data(), ddof=1)
        return self._s

    def s0(self):
        if self._s0 is None:
            self._s0 = np.std(self.data())
        return self._s0

    def __len__(self):
        return self.n()

    def describe(self):
        s = self.s()
        print("Sample {name}: m={m}, s={s}, s^2={s2}".format(
            name=self._name,
            m=self.mean(),
            s=s,
            s2=s*s
        ))
