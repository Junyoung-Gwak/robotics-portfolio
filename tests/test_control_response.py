import math
import unittest
from labs.control_response import advance, simulate


class FirstOrderResponseTest(unittest.TestCase):
    def test_one_time_constant(self):
        self.assertAlmostEqual(advance(0, 1, 0.55, 0.55), 1 - math.exp(-1))

    def test_substeps_match_exact_update(self):
        x = 0.1
        for _ in range(10):
            x = advance(x, 0.8, 0.1, 0.55)
        self.assertAlmostEqual(x, advance(0.1, 0.8, 1.0, 0.55))

    def test_sample_order_at_braking_command(self):
        rows = {s.time: s for s in simulate()}
        self.assertEqual(rows[8.5].command, 0)
        self.assertGreater(rows[8.5].speed, rows[8.55].speed)
        self.assertGreater(rows[8.55].speed, 0)

    def test_zero_duration_still_has_initial_sample(self):
        self.assertEqual(len(simulate(duration=0)), 1)
        with self.assertRaises(ValueError):
            simulate(dt=0)
