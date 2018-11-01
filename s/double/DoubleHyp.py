from ..Hyp import Hyp, AltHypKind


class DoubleHyp(Hyp):
    """Double sample hypothesis"""

    def __init__(self, dist, kind=AltHypKind.TWO_SIDED):
        super(DoubleHyp, self).__init__(dist, kind)

    def criterion(self, sample1, sample2):
        pass

    def test(self, sample1, sample2, alpha):
        _, _, _, result = self.full_test(sample1, sample2, alpha)
        return result

    def full_test(self, sample1, sample2, alpha):
        criterion_value = self.criterion(sample1, sample2)
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
