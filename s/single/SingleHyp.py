from s import AltHypKind, Hyp


class SingleHyp(Hyp):
    """Single sample hypothesis"""

    def __init__(self, dist, kind=AltHypKind.TWO_SIDED):
        super(SingleHyp, self).__init__(dist, kind)

    def criterion(self, sample):
        pass

    def test(self, sample, alpha):
        criterion_value = self.criterion(sample)
        critical_value = self.critical_value(alpha)

        if self.kind == AltHypKind.TWO_SIDED:
            return abs(criterion_value) < critical_value
        if self.kind == AltHypKind.LEFT:
            return criterion_value > critical_value
        if self.kind == AltHypKind.RIGHT:
            return criterion_value < critical_value
