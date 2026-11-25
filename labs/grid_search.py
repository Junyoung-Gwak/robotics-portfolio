"""Dijkstra and A* on the same synthetic four-connected grid, with unit step cost."""
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count

Cell = tuple[int, int]
MOVES: tuple[Cell, ...] = ((1, 0), (0, -1), (-1, 0), (0, 1))


@dataclass(frozen=True)
class Grid:
    width: int
    height: int
    blocked: frozenset[Cell]

    def free(self, cell: Cell) -> bool:
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height and cell not in self.blocked

    def neighbors(self, cell: Cell):
        for dx, dy in MOVES:
            nxt = cell[0] + dx, cell[1] + dy
            if self.free(nxt):
                yield nxt


@dataclass
class Result:
    path: list[Cell]
    expanded: list[Cell]

    @property
    def cost(self) -> int | None:
        return len(self.path) - 1 if self.path else None


def search(grid: Grid, start: Cell, goal: Cell, *, astar: bool) -> Result:
    if not grid.free(start) or not grid.free(goal):
        return Result([], [])
    def estimate(cell: Cell) -> int:
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]) if astar else 0
    order = count()
    front = [(estimate(start), next(order), 0, start)]
    distance = {start: 0}
    parent: dict[Cell, Cell] = {}
    expanded = []
    while front:
        _, _, g, cell = heappop(front)
        if g != distance[cell]:
            continue
        expanded.append(cell)
        if cell == goal:
            path = [goal]
            while path[-1] != start:
                path.append(parent[path[-1]])
            return Result(path[::-1], expanded)
        for nxt in grid.neighbors(cell):
            step = g + 1
            if step < distance.get(nxt, float("inf")):
                distance[nxt], parent[nxt] = step, cell
                heappush(front, (step + estimate(nxt), next(order), step, nxt))
    return Result([], expanded)


def example() -> tuple[Grid, Cell, Cell]:
    obstacles = set()
    for x0, y0, x1, y1 in ((5, 4, 7, 10), (10, 1, 12, 6), (14, 7, 17, 9), (2, 1, 4, 2)):
        obstacles.update((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))
    return Grid(22, 13, frozenset(obstacles)), (2, 9), (18, 2)


if __name__ == "__main__":
    grid, start, goal = example()
    for label, flag in (("Dijkstra", False), ("A* (Manhattan)", True)):
        result = search(grid, start, goal, astar=flag)
        print(f"{label}: path cost={result.cost}, expanded={len(result.expanded)}")
