import unittest

from labs.scan_evidence import scenes, score


class ScanEvidenceTest(unittest.TestCase):
    def test_shared_structure_is_ambiguous(self):
        _, scan, left, right = next(scenes())
        self.assertEqual(score(scan, left, 0.25), score(scan, right, 0.25))

    def test_median_can_hide_a_distinctive_corner(self):
        _, scan, left, right = list(scenes())[1]
        a, b = score(scan, left, 0.25), score(scan, right, 0.25)
        self.assertEqual((a.coverage, b.coverage), (1.0, 0.8))
        self.assertEqual(a.median_distance, b.median_distance)
        self.assertGreater(b.p90_distance, a.p90_distance)

    def test_boundary_is_inclusive_and_scan_order_irrelevant(self):
        scan = [(0.25, 0), (0.5, 0)]
        result = score(scan, [(0, 0)], 0.25)
        self.assertEqual(result.matched, 1)
        self.assertEqual(result, score(list(reversed(scan)), [(0, 0)], 0.25))

    def test_rejects_unknown_observations(self):
        for scan, points, radius in [
            ([], [(0, 0)], 1), ([(0, 0)], [], 1),
            ([(float("nan"), 0)], [(0, 0)], 1),
            ([(0, 0)], [(0, 0)], -1),
        ]:
            with self.subTest(scan=scan, points=points, radius=radius):
                with self.assertRaises(ValueError):
                    score(scan, points, radius)
