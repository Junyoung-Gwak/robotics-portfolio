import unittest
from labs.grid_search import Grid, example, search


class SearchTest(unittest.TestCase):
    def test_same_optimal_cost_and_valid_edges(self):
        grid, start, goal = example()
        baseline = search(grid, start, goal, astar=False)
        guided = search(grid, start, goal, astar=True)
        self.assertEqual(baseline.cost, guided.cost)
        for result in (guided, baseline):
            self.assertEqual(result.path[0], start)
            self.assertEqual(result.path[-1], goal)
            for a, b in zip(result.path, result.path[1:]):
                self.assertIn(b, list(grid.neighbors(a)))
        self.assertLess(len(guided.expanded), len(baseline.expanded))

    def test_barrier_is_unreachable(self):
        grid = Grid(3, 3, frozenset((1, y) for y in range(3)))
        for mode in (True, False):
            result = search(grid, (0, 1), (2, 1), astar=mode)
            self.assertEqual(result.path, [])
            self.assertIsNone(result.cost)

    def test_trivial_route_and_invalid_endpoints(self):
        grid = Grid(2, 2, frozenset({(1, 1)}))
        self.assertEqual(search(grid,(0,0),(0,0),astar=True).cost, 0)
        self.assertIsNone(search(grid,(0,0),(1,1),astar=True).cost)
        self.assertIsNone(search(grid,(-1,0),(0,0),astar=True).cost)

    def test_open_grid_matches_manhattan_distance(self):
        result=search(Grid(6,5,frozenset()),(0,0),(5,4),astar=True)
        self.assertEqual(result.cost,9)
