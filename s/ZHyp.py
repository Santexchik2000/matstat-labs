from scipy import stats
import numpy as np
from .Hyp import Hyp


class ZHyp(Hyp):
    """z-test"""
    def __init__(self, kind, m, sigma):
        super(ZHyp, self).__init__(stats.norm, kind=kind)
        self.m = m
        self.sigma = sigma

    def criterion(self, sample):
        mean = np.mean(sample)
        n = len(sample)
        return (mean - self.m) / self.sigma * np.sqrt(n)

    def critical_value(self, alpha):
        return super(ZHyp, self).critical_value(alpha, 0, 1)

    def p_value(self, criterion_value):
        return super(ZHyp, self).p_value(criterion_value, 0, 1)

    def test(self, sample, alpha):
        return super(ZHyp, self).test(sample, alpha, 0, 1)
