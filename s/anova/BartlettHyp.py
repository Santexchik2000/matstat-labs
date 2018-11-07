from scipy.stats import bartlett, chi2
from ..Hyp import Hyp, AltHypKind


class BartlettHyp(Hyp):
    def __init__(self, groups):
        k = groups.num_groups()
        dist = chi2(k - 1)
        super(BartlettHyp, self).__init__(dist=dist, kind=AltHypKind.RIGHT)

    def full_test(self, groups, alpha):
        list_of_data = [sample.data() for sample in groups.groups()]
        (criterion_value, p_value) = bartlett(*list_of_data)

        crit_left, crit_right = self.critical_values(alpha)

        return criterion_value, (crit_left, crit_right), p_value, criterion_value < crit_right
