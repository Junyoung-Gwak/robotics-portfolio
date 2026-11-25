"""Score fixed poses against two synthetic point sets, without fitting a pose."""

from dataclasses import dataclass
from math import ceil, dist, isfinite
from statistics import median

Point = tuple[float, float]


@dataclass(frozen=True)
class Score:
    matched: int
    total: int
    median_distance: float
    p90_distance: float

    @property
    def coverage(self) -> float:
        return self.matched / self.total


def score(scan: list[Point], reference: list[Point], radius: float) -> Score:
    if not scan or not reference:
        raise ValueError("Both point sets must contain observations")
    if not isfinite(radius) or radius < 0:
        raise ValueError("The matching radius must be finite and nonnegative")
    for points in (scan, reference):
        if any(len(point) != 2 or not all(map(isfinite, point)) for point in points):
            raise ValueError("Expected finite 2D coordinates")
    distances = sorted(min(dist(p, q) for q in reference) for p in scan)
    return Score(
        matched=sum(value <= radius for value in distances),
        total=len(distances),
        median_distance=median(distances),
        p90_distance=distances[ceil(0.90 * len(distances)) - 1],
    )


def scenes():
    shared = [(float(x), 0.0) for x in range(8)]
    left = shared + [(2.0, 1.0), (2.0, 2.0)]
    right = shared + [(5.0, 1.0), (5.0, 2.0)]
    for name, visible in [("shared only", shared), ("with corner", left)]:
        scan = [(x + 0.125, y) for x, y in visible]
        yield name, scan, left, right


if __name__ == "__main__":
    for scene, scan, left, right in scenes():
        for label, points in [("A", left), ("B", right)]:
            result = score(scan, points, radius=0.25)
            print(f"{scene:12} {label}  {result.matched}/{result.total}  "
                  f"median={result.median_distance:.3f}  p90={result.p90_distance:.3f}")
