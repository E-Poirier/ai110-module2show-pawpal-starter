from __future__ import annotations

from pawpal.models import (
    DayPlan,
    Owner,
    Pet,
    PRIORITY_RANK,
    ScheduledBlock,
    Task,
)


def _sort_key(task: Task) -> tuple[int, int, str]:
    """Higher priority first; shorter duration next; stable title tie-break."""
    return (-PRIORITY_RANK[task.priority], task.duration_minutes, task.title)


def build_daily_plan(
    owner: Owner,
    pet: Pet,
    tasks: list[Task],
    available_minutes: int,
) -> DayPlan:
    """
    Build a greedy daily plan: higher-priority tasks first, pack until the
    time budget is exhausted. Tasks that do not fit are recorded in skipped_tasks.
    """
    plan = DayPlan(owner=owner, pet=pet, available_minutes=available_minutes)
    if available_minutes <= 0:
        for t in tasks:
            plan.skipped_tasks.append((t, "No time available in today's budget."))
        return plan

    ordered = sorted(tasks, key=_sort_key)
    cursor = 0
    remaining = available_minutes

    for task in ordered:
        if task.duration_minutes > remaining:
            if task.duration_minutes > available_minutes:
                plan.skipped_tasks.append(
                    (
                        task,
                        f"Task needs {task.duration_minutes} min; only {available_minutes} min available today.",
                    )
                )
            else:
                plan.skipped_tasks.append(
                    (
                        task,
                        f"Not enough remaining time ({remaining} min left; needs {task.duration_minutes} min).",
                    )
                )
            continue

        reason = (
            f"{task.priority.capitalize()} priority; starts at minute {cursor}; "
            f"{remaining - task.duration_minutes} min left in budget after this block."
        )
        plan.scheduled.append(
            ScheduledBlock(task=task, start_minute=cursor, reason=reason)
        )
        cursor += task.duration_minutes
        remaining -= task.duration_minutes

    return plan
