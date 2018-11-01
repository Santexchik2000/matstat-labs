from enum import Enum


class AltHypKind(Enum):
    LEFT = -1
    RIGHT = 1
    TWO_SIDED = 0


class Hyp(object):
    dist = None
    kind = None

    def __init__(self, dist, kind=AltHypKind.TWO_SIDED):
        self.dist = dist
        self.kind = kind

    def critical_values(self, alpha):
        level = alpha / 2 if self.kind == AltHypKind.TWO_SIDED else alpha
        return self.dist.ppf(level), self.dist.ppf(1 - level)

    def p_value(self, criterion_value):
        left_p = self.dist.cdf(criterion_value)
        if self.kind == AltHypKind.LEFT:
            return left_p
        if self.kind == AltHypKind.RIGHT:
            return 1 - left_p
        if self.kind == AltHypKind.TWO_SIDED:
            return 2 * min(left_p, 1 - left_p)
