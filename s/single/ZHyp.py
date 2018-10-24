from scipy import stats
import numpy as np
from s.Hyp import Hyp


class ZHyp(Hyp):
    """z-test"""
    def __init__(self, kind, m, sigma):
        super(ZHyp, self).__init__(stats.norm(0, 1), kind=kind)
        self.m = m
        self.sigma = sigma

    def criterion(self, sample):
        mean = sample.mean()
        n = sample.n()
        return (mean - self.m) / self.sigma * np.sqrt(n)
