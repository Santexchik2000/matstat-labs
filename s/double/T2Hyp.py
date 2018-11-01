from scipy import stats
import numpy as np
from .DoubleHyp import DoubleHyp


class T2Hyp(DoubleHyp):
    """double T-test hypothesis"""
    def __init__(self, kind, sample1, sample2):
        n1 = sample1.n()
        n2 = sample2.n()
        dist = stats.t(n1 + n2 - 2)
        super(T2Hyp, self).__init__(dist, kind=kind)

    def criterion(self, sample1, sample2):
        n1 = sample1.n() - 1
        n2 = sample2.n() - 1
        s1 = sample1.s()
        s2 = sample2.s()
        S = (n1 * s1 * s1 + n2 * s2 * s2) / (n1 + n2)

        m1 = sample1.mean()
        m2 = sample2.mean()
        return (m1 - m2) / (S * np.sqrt(1. / (n1 + 1) + 1. / (n2 + 1)))
