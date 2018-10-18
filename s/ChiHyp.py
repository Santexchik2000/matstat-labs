from scipy import stats
import numpy as np
from .Hyp import Hyp


class ChiHyp(Hyp):
    """chi-squared-test"""
    def __init__(self, kind, sigma, m=None):
        super(ChiHyp, self).__init__(stats.chi2, kind=kind)
        self.m = m
        self.sigma = sigma

    def criterion(self, sample):
        n = len(sample)
        if self.m is None:
            s = np.var(sample, ddof=1)
            return (n - 1) * ((s / self.sigma) ** 2)
        else:
            s0_square = np.mean((sample - self.m) ** 2)
            return n * s0_square / self.sigma / self.sigma

    def critical_value(self, alpha, n):
        if self.m is None:
            return super(ChiHyp, self).critical_value(alpha, n - 1)
        else:
            return super(ChiHyp, self).critical_value(alpha, n)

    def p_value(self, criterion_value, n):
        if self.m is None:
            return super(ChiHyp, self).p_value(criterion_value, n - 1)
        else:
            return super(ChiHyp, self).p_value(criterion_value, n)

    def test(self, sample, alpha):
        if self.m is None:
            return super(ChiHyp, self).test(sample, alpha, len(sample) - 1)
        else:
            return super(ChiHyp, self).test(sample, alpha, len(sample))
