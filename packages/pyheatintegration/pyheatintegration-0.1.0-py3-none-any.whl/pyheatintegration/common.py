from typing import Tuple


def minmax(a: float, b: float) -> Tuple[float, float]:
    if a > b:
        return b, a
    return a, b


class Range:
    start: float
    finish: float
    delta: float
    min_: float
    max_: float

    def __init__(self, start: float, finish: float):
        self.start = start
        self.finish = finish
        self.delta = self.finish - self.start
        self.min_, self.max_ = minmax(self.start, self.finish)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return self.start == other.start and self.finish == other.finish

    def __ne__(self, other) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return self.start < other.start

    def __le__(self, other) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return self.start <= other.start

    def __gt__(self, other) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return self.start > other.start

    def __ge__(self, other) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return self.start >= other.start

    def __hash__(self) -> int:
        return hash((self.start, self.finish))

    def __str__(self) -> str:
        return f"{self.start}->{self.finish}"

    def __format__(self, format_spec: str) -> str:
        return f"{self.start.__format__(format_spec)}->{self.finish.__format__(format_spec)}"

    def range(self) -> Tuple[float, float]:
        return self.min_, self.max_

    def shift(self, delta: float) -> None:
        self.start += delta
        self.finish += delta
        self.min_ += delta
        self.max_ += delta
