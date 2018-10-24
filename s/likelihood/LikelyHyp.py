from s.Hyp import Hyp, AltHypKind


class Likely2SampleHyp(Hyp):
    """2-samples likelihood hypothesis"""
    def __init__(self, dist, kind=AltHypKind.TWO_SIDED):
        super(Likely2SampleHyp, self).__init__(dist, kind)

    def criterion(self, sample1, sample2):
        pass

    def test(self, sample1, sample2, alpha=0.05):
        pass

    def full_test(self, sample1, sample2, alpha=0.05):
        pass


class Likely1SampleHyp(Hyp):
    """1 sample vs distribution likelihood hypothesis"""

    def __init__(self, dist, kind=AltHypKind.TWO_SIDED):
        super(Likely1SampleHyp, self).__init__(dist, kind)

    def criterion(self, dist, sample):
        pass

    def test(self, dist, sample, alpha=0.05):
        pass

    def full_test(self, dist, sample, alpha=0.05):
        pass
