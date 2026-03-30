"""Tests importing the public API through `pawpal_system` (CodePath layout)."""

import pytest

from pawpal_system import Owner, Pet, Scheduler, Task, build_daily_plan


@pytest.fixture
def ctx():
    return Owner("Jordan"), Pet("Mochi", "dog")


def test_empty_tasks_returns_empty_plan(ctx):
    owner, pet = ctx
    plan = build_daily_plan(owner, pet, [], available_minutes=120)
    assert plan.scheduled == []
    assert plan.skipped_tasks == []
    assert plan.total_scheduled_minutes == 0


def test_scheduler_class_matches_build_daily_plan(ctx):
    owner, pet = ctx
    tasks = [Task("walk", 15, "high")]
    plan_fn = build_daily_plan(owner, pet, tasks, 60)
    plan_cls = Scheduler().build_daily_plan(owner, pet, tasks, 60)
    assert len(plan_fn.scheduled) == len(plan_cls.scheduled) == 1
    assert plan_fn.scheduled[0].task.title == plan_cls.scheduled[0].task.title


def test_priority_order_when_all_fit(ctx):
    owner, pet = ctx
    tasks = [
        Task("low task", 10, "low"),
        Task("high task", 10, "high"),
        Task("med task", 10, "medium"),
    ]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=60)
    titles = [b.task.title for b in plan.scheduled]
    assert titles == ["high task", "med task", "low task"]


def test_budget_drops_lower_priority(ctx):
    owner, pet = ctx
    tasks = [
        Task("high", 40, "high"),
        Task("low", 40, "low"),
    ]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=50)
    assert len(plan.scheduled) == 1
    assert plan.scheduled[0].task.title == "high"
    assert len(plan.skipped_tasks) == 1


def test_zero_budget_skips_tasks(ctx):
    owner, pet = ctx
    tasks = [Task("walk", 10, "high")]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=0)
    assert plan.scheduled == []
    assert len(plan.skipped_tasks) == 1
