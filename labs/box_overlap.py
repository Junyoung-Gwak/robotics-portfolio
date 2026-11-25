"""Compare union-normalized and smaller-box-normalized overlap on synthetic boxes."""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Box:
    left: float
    top: float
    right: float
    bottom: float

    def __post_init__(self) -> None:
        if not all(isfinite(v) for v in (self.left, self.top, self.right, self.bottom)):
            raise ValueError("Box coordinates must be finite")
        if self.right <= self.left or self.bottom <= self.top:
            raise ValueError("Box must have positive width and height")

    @property
    def area(self) -> float:
        return (self.right - self.left) * (self.bottom - self.top)


@dataclass(frozen=True)
class Overlap:
    iou: float
    fraction_of_smaller: float


def measure(a: Box, b: Box) -> Overlap:
    width = max(0.0, min(a.right, b.right) - max(a.left, b.left))
    height = max(0.0, min(a.bottom, b.bottom) - max(a.top, b.top))
    intersection = width * height
    union = a.area + b.area - intersection
    return Overlap(intersection / union, intersection / min(a.area, b.area))


def examples() -> dict[str, tuple[Box, Box]]:
    return {
        "Nested": (Box(0, 0, 10, 8), Box(2, 2, 4, 4)),
        "Crossing": (Box(0, 0, 5, 4), Box(3, 0, 8, 4)),
        "Separated": (Box(0, 0, 4, 4), Box(6, 0, 10, 4)),
    }


if __name__ == "__main__":
    for name, pair in examples().items():
        scores = measure(*pair)
        print(f"{name}: IoU={scores.iou:.2f}, smaller-box overlap={scores.fraction_of_smaller:.2f}")
