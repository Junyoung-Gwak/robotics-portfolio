import itertools
import unittest

from labs.mission_replay import Event, Signal, Stage, advance, example


class HandoffTest(unittest.TestCase):
    def test_other_request_cannot_change_any_stage(self):
        for stage, signal in itertools.product(Stage, Signal):
            self.assertEqual(advance("current", stage, Event("old", signal)).stage, stage)

    def test_only_one_order_can_complete_in_four_events(self):
        completed = []
        for signals in itertools.product(Signal, repeat=4):
            stage = Stage.WAIT_ENTRY
            for signal in signals:
                stage = advance("current", stage, Event("current", signal)).stage
            if stage == Stage.DONE:
                completed.append(signals)
        self.assertEqual(completed, [(Signal.ENTRY_ALLOWED, Signal.ENTRY_COMPLETE,
                                      Signal.EXIT_ALLOWED, Signal.EXIT_COMPLETE)])

    def test_done_is_terminal_even_when_messages_repeat(self):
        for signal in Signal:
            self.assertEqual(advance("active", Stage.DONE, Event("active", signal)).stage,
                             Stage.DONE)

    def test_delayed_and_duplicate_messages_in_example(self):
        stage = Stage.WAIT_ENTRY
        reasons = []
        for event in example():
            decision = advance("active", stage, event)
            reasons.append(decision.reason)
            stage = decision.stage
        self.assertEqual(stage, Stage.DONE)
        self.assertEqual(reasons.count("accepted"), 4)
        self.assertEqual(reasons.count("different request"), 1)
        self.assertEqual(reasons.count("unexpected at this stage"), 2)
