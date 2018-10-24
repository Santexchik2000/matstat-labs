from scipy import stats
import numpy as np

from s import AltHypKind
from s.likelihood.LikelyHyp import Likely2SampleHyp, Likely1SampleHyp


def hist_from_cdf(dist, bins):
    ps = [dist.cdf(limit) for limit in bins]
    result = []
    prev = 0
    for i in range(len(ps) - 1):
        result.append(ps[i + 1] - prev)
        prev = ps[i + 1]
    return np.array(result)


class Pierson2SampledHyp(Likely2SampleHyp):
    bins = None
    
    def __init__(self, bins):
        r = len(bins)
        super(Pierson2SampledHyp, self).__init__(
            stats.chi2(r - 1),
            AltHypKind.RIGHT
        )
        self.bins = bins

    def criterion(self, sample1, sample2):
        hist1, _ = np.histogram(sample1.data(), bins=self.bins)
        hist2, _ = np.histogram(sample2.data(), bins=self.bins)
        n1 = sample1.n()
        n2 = sample2.n()
        return n1 * n2 * np.sum(
            1. / (hist1 + hist2) * (hist1 / n1 - hist2 / n2) ** 2
        )

    def test(self, sample1, sample2, alpha=0.05):
        criterion_value = self.criterion(sample1, sample2)
        critical_value = self.critical_value(alpha)
        return criterion_value < critical_value


class Pierson1SampledHyp(Likely1SampleHyp):
    bins = None
    unknown_params_n = None

    def __init__(self, bins, unknown_params_n=0):
        r = len(bins) - 1
        super(Pierson1SampledHyp, self).__init__(
            stats.chi2(r - unknown_params_n - 1),
            AltHypKind.RIGHT
        )
        self.bins = bins
        self.unknown_params_n = unknown_params_n

    def criterion(self, dist, sample):
        hist_real, _ = np.histogram(sample.data(), bins=self.bins)
        hist_expected = hist_from_cdf(dist, bins=self.bins) * sample.n()
        return np.sum(
            (hist_real - hist_expected)**2 / hist_expected
        )

    def test(self, dist, sample, alpha=0.05):
        _, _, _, result = self.full_test(dist, sample, alpha)
        return result

    def full_test(self, dist, sample, alpha=0.05):
        criterion_value = self.criterion(dist, sample)
        critical_value = self.critical_value(alpha)
        p_value = self.p_value(criterion_value)
        return criterion_value, critical_value, p_value, criterion_value < critical_value
