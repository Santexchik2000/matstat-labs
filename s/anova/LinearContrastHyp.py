from scipy import stats
import numpy as np

from ..Hyp import Hyp, AltHypKind


class LinearContrastHyp(Hyp):
    _groups = None
    _dist = None

    def __init__(self, groups):
        k = groups.num_groups()
        n = groups.n()
        dist = stats.f(k - 1, n - k)
        super(LinearContrastHyp, self).__init__(dist=dist, kind=AltHypKind.TWO_SIDED)
        self._groups = groups

    def full_test(self, coeffs, alpha=0.05):
        coeffs = np.array(coeffs)

        groups = self._groups.groups()
        n = self._groups.n()
        k = self._groups.num_groups()
        w_var = self._groups.within_group_var()

        c = np.sum(coeffs * np.array([
            sample.mean() for sample in groups
        ]))

        sigma2C = n * w_var * np.sum(
            coeffs ** 2 / np.array([
                sample.n() for sample in groups
            ])
        ) / (n - k)

        delta = np.sqrt(sigma2C * (k - 1) * self.dist.ppf(alpha))
        p_value = self.p_value(c)

        accept = (c - delta < 0) and (0 < c + delta)

        return c, (c - delta, c + delta), p_value, accept
