"""PawPal+ backend logic layer (CodePath Unit 5 single-module entry point).

The full implementation lives in the `pawpal` package; this file re-exports the
public types and scheduling API so materials can use `import pawpal_system` and
a `Scheduler` class as the system \"brain\".
"""

from __future__ import annotations

from pawpal.models import DayPlan, Owner, Pet, ScheduledBlock, Task
from pawpal.scheduler import build_daily_plan

__all__ = [
    "DayPlan",
    "Owner",
    "Pet",
    "ScheduledBlock",
    "Scheduler",
    "Task",
    "build_daily_plan",
]


class Scheduler:
    """Coordinates building a daily plan (wrapper around `build_daily_plan`)."""

    def build_daily_plan(
        self,
        owner: Owner,
        pet: Pet,
        tasks: list[Task],
        available_minutes: int,
    ) -> DayPlan:
        return build_daily_plan(owner, pet, tasks, available_minutes)
