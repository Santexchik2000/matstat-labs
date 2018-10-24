from scipy import stats
import numpy as np
from s.single.SingleHyp import SingleHyp


class ChiHyp(SingleHyp):
    """chi-squared-test"""
    def __init__(self, kind, sample, sigma, m=None):
        n = sample.n()
        dist = stats.chi2(n - 1) if m is None else stats.chi2(n)
        super(ChiHyp, self).__init__(dist, kind=kind)
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

    def critical_value(self, alpha):
        if self.m is None:
            return super(ChiHyp, self).critical_value(alpha)
        else:
            return super(ChiHyp, self).critical_value(alpha)

    def p_value(self, criterion_value):
        if self.m is None:
            return super(ChiHyp, self).p_value(criterion_value)
        else:
            return super(ChiHyp, self).p_value(criterion_value)

    def test(self, sample, alpha):
        if self.m is None:
            return super(ChiHyp, self).test(sample, alpha)
        else:
            return super(ChiHyp, self).test(sample, alpha)
