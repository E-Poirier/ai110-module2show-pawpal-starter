from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

PriorityLevel = Literal["low", "medium", "high"]

PRIORITY_RANK: dict[PriorityLevel, int] = {
    "low": 1,
    "medium": 2,
    "high": 3,
}


@dataclass(frozen=True)
class Owner:
    """Pet owner display/context."""

    name: str


@dataclass(frozen=True)
class Pet:
    """Pet display/context."""

    name: str
    species: str


@dataclass(frozen=True)
class Task:
    """A single care task."""

    title: str
    duration_minutes: int
    priority: PriorityLevel


@dataclass(frozen=True)
class ScheduledBlock:
    """One task placed on the timeline with a human-readable rationale."""

    task: Task
    start_minute: int
    reason: str


@dataclass
class DayPlan:
    """Result of packing tasks into the day's available minutes."""

    owner: Owner
    pet: Pet
    available_minutes: int
    scheduled: list[ScheduledBlock] = field(default_factory=list)
    skipped_tasks: list[tuple[Task, str]] = field(default_factory=list)

    @property
    def total_scheduled_minutes(self) -> int:
        return sum(b.task.duration_minutes for b in self.scheduled)
