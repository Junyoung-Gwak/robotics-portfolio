"""A first-order speed response driven by a synthetic piecewise-constant command."""
from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class Sample:
    time: float
    command: float
    speed: float


def commanded_speed(t: float) -> float:
    for end, speed in ((1.0, 0.0), (4.0, 0.8), (6.5, 0.25), (8.5, 0.6)):
        if t < end:
            return speed
    return 0.0


def advance(speed: float, command: float, dt: float, tau: float) -> float:
    if dt < 0 or tau <= 0:
        raise ValueError("dt must be non-negative and tau must be positive")
    return command + (speed - command) * exp(-dt / tau)


def simulate(dt: float = 0.05, tau: float = 0.55, duration: float = 10.0) -> list[Sample]:
    if dt <= 0 or duration < 0 or tau <= 0:
        raise ValueError("dt and tau must be positive and duration non-negative")
    # Sample at k*dt. The command at k drives the interval [k*dt, (k+1)*dt).
    speed = 0.0
    samples = []
    for k in range(int(round(duration / dt)) + 1):
        t = round(k * dt, 10)
        if t > duration:
            break
        command = commanded_speed(t)
        samples.append(Sample(t, command, speed))
        speed = advance(speed, command, dt, tau)
    return samples


if __name__ == "__main__":
    import csv
    import sys
    writer = csv.writer(sys.stdout)
    writer.writerow(["time_s", "command_m_s", "modeled_speed_m_s"])
    for s in simulate():
        writer.writerow([s.time, s.command, round(s.speed, 6)])
