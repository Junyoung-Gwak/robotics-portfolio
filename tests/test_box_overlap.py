import unittest
from labs.box_overlap import Box, examples, measure


class BoxOverlapTest(unittest.TestCase):
    def test_containment_can_have_small_iou(self):
        scores = measure(*examples()["Nested"])
        self.assertAlmostEqual(scores.iou, 0.05)
        self.assertEqual(scores.fraction_of_smaller, 1.0)

    def test_crossing_boxes_and_symmetry(self):
        a, b = examples()["Crossing"]
        self.assertEqual(measure(a, b), measure(b, a))
        self.assertAlmostEqual(measure(a, b).iou, 0.25)
        self.assertAlmostEqual(measure(a, b).fraction_of_smaller, 0.4)

    def test_touching_edge_has_no_area(self):
        a, b = Box(0, 0, 1, 1), Box(1, 0, 2, 1)
        self.assertEqual(measure(a, b).iou, 0.0)
        self.assertEqual(measure(a, b).fraction_of_smaller, 0.0)

    def test_invalid_geometry_is_rejected(self):
        for coordinates in ((0, 0, 0, 1), (0, 0, 1, float("nan"))):
            with self.subTest(coordinates=coordinates):
                with self.assertRaises(ValueError):
                    Box(*coordinates)
