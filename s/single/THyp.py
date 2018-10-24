from scipy import stats
import numpy as np
from s.Hyp import Hyp


class THyp(Hyp):
    """t-test"""
    m = None

    def __init__(self, kind, m, sample):
        super(THyp, self).__init__(stats.t(sample.n() - 1), kind=kind)
        self.m = m

    def criterion(self, sample):
        s = sample.s()
        mean = sample.mean()
        n = sample.n()
        return (mean - self.m) / s * np.sqrt(n)

    def test(self, sample, alpha, *args):
        return super(THyp, self).test(sample, alpha)
