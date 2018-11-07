import numpy as np
from s.Sample import Sample


class PooledSample(Sample):
    _groups = []

    def __init__(self, name, *samples):
        super(PooledSample, self).__init__(name)
        self._groups = samples

    def groups(self):
        return [g for g in self._groups]

    def at(self, i):
        return self._groups[i]

    def data(self):
        return np.concatenate([sample.data() for sample in self._groups])

    def n(self):
        return np.sum(
            np.array([sample.n() for sample in self._groups])
        )

    def num_groups(self):
        return len(self._groups)

    def mean(self):
        return np.sum(
            np.array([sample.n() * sample.mean() for sample in self._groups])
        ) / self.n()

    def within_group_var(self):
        return np.sum(
            np.array([sample.n() * sample.s0() ** 2 for sample in self._groups])
        ) / self.n()

    def between_group_var(self):
        mean = self.mean()
        return np.sum(
            np.array([
                sample.n() * (sample.mean() - mean) ** 2 for sample in self._groups
            ])
        ) / self.n()

    def var(self):
        return self.within_group_var() + self.between_group_var()

    def s0(self):
        return np.sqrt(self.var())

    def eta_squared(self):
        return self.between_group_var() / self.var()

    def merge(self, name=None):
        if name is None:
            name = self._name + " merged"
        return Sample.from_data(name, self.data())

