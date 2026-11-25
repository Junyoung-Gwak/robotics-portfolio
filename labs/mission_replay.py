"""Replay a synthetic handoff between a facility and a robot. No hardware I/O."""
from dataclasses import dataclass
from enum import Enum


class Stage(Enum):
    WAIT_ENTRY = "waiting for entry permission"
    ENTERING = "entering"
    WAIT_EXIT = "waiting for exit permission"
    EXITING = "exiting"
    DONE = "complete"


class Signal(Enum):
    ENTRY_ALLOWED = "entry allowed"
    ENTRY_COMPLETE = "entry complete"
    EXIT_ALLOWED = "exit allowed"
    EXIT_COMPLETE = "exit complete"


TRANSITIONS = {
    (Stage.WAIT_ENTRY, Signal.ENTRY_ALLOWED): Stage.ENTERING,
    (Stage.ENTERING, Signal.ENTRY_COMPLETE): Stage.WAIT_EXIT,
    (Stage.WAIT_EXIT, Signal.EXIT_ALLOWED): Stage.EXITING,
    (Stage.EXITING, Signal.EXIT_COMPLETE): Stage.DONE,
}


@dataclass(frozen=True)
class Event:
    request: str
    signal: Signal


@dataclass(frozen=True)
class Decision:
    stage: Stage
    reason: str


def advance(request: str, stage: Stage, event: Event) -> Decision:
    if event.request != request:
        return Decision(stage, "different request")
    following = TRANSITIONS.get((stage, event.signal))
    if following is None:
        return Decision(stage, "unexpected at this stage")
    return Decision(following, "accepted")


def example():
    return [
        Event("earlier", Signal.ENTRY_ALLOWED),
        Event("active", Signal.ENTRY_ALLOWED),
        Event("active", Signal.ENTRY_ALLOWED),
        Event("active", Signal.EXIT_ALLOWED),
        Event("active", Signal.ENTRY_COMPLETE),
        Event("active", Signal.EXIT_ALLOWED),
        Event("active", Signal.EXIT_COMPLETE),
    ]


if __name__ == "__main__":
    stage = Stage.WAIT_ENTRY
    for item in example():
        result = advance("active", stage, item)
        print(f"{item.request:7} {item.signal.value:15} {result.reason:25} {result.stage.value}")
        stage = result.stage
