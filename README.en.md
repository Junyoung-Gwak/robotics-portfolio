# Junyoung Gwak · Robotics software engineer

[한국어 포트폴리오](README.md)

I work on mobile robots that follow people, patrol between waypoints and coordinate with building equipment. When a robot stops unexpectedly, I trace the observation, selected path, issued command and reported state at the same point in time.

### Selected work, most recent first

| Work | My contribution | What I verified |
| --- | --- | --- |
| Person-following navigation · November 2026 | Checked the robot footprint along candidate detours and traced the selected path into the command output. | An existing synthetic regression rejected the blocked straight path, selected a detour and produced a forward command. [Case in Korean](projects/navigation.md) |
| Multi-floor localization · November 2026 | Compared the same scan against two floor hypotheses and traced how an operator-supplied initial pose reached the estimator. | A field check recovered tracking on one floor. Absolute pose accuracy and repeatability across floors need independent measurements. [Case in Korean](projects/localization.md) |
| Patrol and elevator integration · August–November 2026 | Investigated repeated waypoint deceleration and linked facility permissions to the active robot request and mission stage. | Observed one complete elevator mission through boarding, exit and return to idle. [Integration case in Korean](projects/integration.md) |
| Vehicle tracking · June–July 2026 | Compared trackers on identical detections and inspected nested boxes before track assignment. | The reviewed segment had fewer output boxes and unique IDs. Ground-truth tracks would be needed to measure false merges or ID switches. [Case in Korean](projects/perception.md) |
| Robot workcells · January–March 2026 | Led three training teams. I integrated the logistics cell, handled UI and integration for block assembly, and worked on UI, control and recovery for the lettering robot. | The case study lists responsibilities separately for each team. [Workcell projects in Korean](projects/robot-cells.md) |

### Reproduce a technical example

| Question | Example | Condition that matters |
| --- | --- | --- |
| Why does A* expand fewer cells here? | [Nine-second animation and source](labs/path-search.md) | On this four-connected grid, Manhattan distance is admissible. Both searches return cost 27. |
| When can floor hypotheses tie? | [Nearest-neighbor scan scoring](labs/scan-evidence.md) | If the scan contains only the shared wall, both candidates explain all eight points. |
| Why can a contained detection have low IoU? | [Box geometry](labs/box-overlap.md) | A small box entirely inside a large one can have full containment and small intersection over union. |
| Why can speed remain positive after a zero command? | [First-order speed model](labs/control-response.md) | With a finite time constant, model speed decays over time after a step down to zero. |

The examples and illustrations were created specifically for this portfolio using synthetic inputs. Project dates above refer to the original work. Run the examples with Python 3.10 or later from the repository root. No robot hardware is required.

```sh
python -m labs.grid_search
python -m unittest discover -s tests -v
```
