from scipy import stats
from ..Hyp import Hyp, AltHypKind


class OneWayAnovaHyp(Hyp):
    """One way ANOVA hypothesis"""
    def __init__(self, groups):
        n = groups.n()
        k = groups.num_groups()
        dist = stats.f(k - 1, n - k)
        super(OneWayAnovaHyp, self).__init__(dist, kind=AltHypKind.RIGHT)

    def criterion(self, groups):
        return (
            groups.between_group_var() / (groups.num_groups() - 1)
        ) / (
            groups.within_group_var() / (groups.n() - groups.num_groups())
        )

    def test(self, sample, alpha):
        _, _, _, result = self.full_test(sample, alpha)
        return result

    def full_test(self, sample, alpha):
        criterion_value = self.criterion(sample)
        crit_left, crit_right = self.critical_values(alpha)

        p_value = self.p_value(criterion_value)

        result = False

        if self.kind == AltHypKind.TWO_SIDED:
            result = (crit_left < criterion_value) and (criterion_value < crit_right)
        if self.kind == AltHypKind.LEFT:
            result = crit_left < criterion_value
        if self.kind == AltHypKind.RIGHT:
            result = criterion_value < crit_right

        return criterion_value, (crit_left, crit_right), p_value, result
