from scipy import stats
from .DoubleHyp import DoubleHyp, AltHypKind


class FHyp(DoubleHyp):
    """F-test hypothesis"""
    def __init__(self, kind, sample1, sample2, m=None):
        n1 = sample1.n()
        n2 = sample2.n()
        dist = stats.f(n1 - 1, n2 - 1) if m is None else stats.f(n1, n2)
        super(FHyp, self).__init__(dist, kind=kind)
        self.m = m

    def criterion(self, sample1, sample2):
        if self.m is None:
            s1 = sample1.s() ** 2
            s2 = sample2.s() ** 2
            return max(s1, s2) / min(s1, s2)
        else:
            s01 = sample1.s0() ** 2
            s02 = sample2.s0() ** 2
            return max(s01, s02) / min(s01, s02)
