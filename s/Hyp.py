from enum import Enum


class AltHypKind(Enum):
    LEFT = -1
    RIGHT = 1
    TWO_SIDED = 0


class Hyp(object):
    """Hypothesis"""
    dist = None
    kind = None

    def __init__(self, dist, kind=AltHypKind.TWO_SIDED):
        self.dist = dist
        self.kind = kind

    def criterion(self, sample):
        pass

    def critical_value(self, alpha, *args):
        level = 1 - alpha / 2 if self.kind == AltHypKind.TWO_SIDED else 1 - alpha
        return self.dist.ppf(level, *args)

    def p_value(self, criterion_value, *args):
        left_p = self.dist.cdf(criterion_value, *args)
        if self.kind == AltHypKind.LEFT:
            return left_p
        if self.kind == AltHypKind.RIGHT:
            return 1 - left_p
        if self.kind == AltHypKind.TWO_SIDED:
            return 2 * min(left_p, 1 - left_p)

    def test(self, sample, alpha, *args):
        criterion_value = self.criterion(sample)
        critical_value = self.critical_value(alpha, *args)

        if self.kind == AltHypKind.TWO_SIDED:
            return abs(criterion_value) < critical_value
        if self.kind == AltHypKind.LEFT:
            return criterion_value > critical_value
        if self.kind == AltHypKind.RIGHT:
            return criterion_value < critical_value
