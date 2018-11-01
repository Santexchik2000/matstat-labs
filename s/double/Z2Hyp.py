from scipy import stats
import numpy as np
from .DoubleHyp import DoubleHyp


class Z2Hyp(DoubleHyp):
    """double Z-test hypothesis"""
    def __init__(self, kind, sigma1, sigma2):
        dist = stats.norm(0, 1)
        super(Z2Hyp, self).__init__(dist, kind=kind)
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def criterion(self, sample1, sample2):
        m1 = sample1.mean()
        m2 = sample2.mean()
        sigmas = self.sigma1 ** 2 / sample1.n() + self.sigma2 ** 2 / sample2.n()
        return (m1 - m2) / np.sqrt(sigmas)
