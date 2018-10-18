from scipy import stats
import numpy as np
from .Hyp import Hyp


class THyp(Hyp):
    """t-test"""
    def __init__(self, kind, m):
        super(THyp, self).__init__(stats.t, kind=kind)
        self.m = m

    def criterion(self, sample):
        s = np.std(sample, ddof=1)
        mean = np.mean(sample)
        return (mean - self.m) / s * np.sqrt(len(sample))

    def test(self, sample, alpha, *args):
        return super(THyp, self).test(sample, alpha, len(sample) - 1)
