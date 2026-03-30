import pytest

from pawpal.models import Owner, Pet, Task
from pawpal.scheduler import build_daily_plan


@pytest.fixture
def ctx():
    return Owner("Jordan"), Pet("Mochi", "dog")


def test_empty_tasks_returns_empty_plan(ctx):
    owner, pet = ctx
    plan = build_daily_plan(owner, pet, [], available_minutes=120)
    assert plan.scheduled == []
    assert plan.skipped_tasks == []
    assert plan.total_scheduled_minutes == 0


def test_all_tasks_fit_in_order_of_priority_then_duration(ctx):
    owner, pet = ctx
    tasks = [
        Task("low task", 10, "low"),
        Task("high task", 10, "high"),
        Task("med task", 10, "medium"),
    ]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=60)
    assert len(plan.scheduled) == 3
    titles = [b.task.title for b in plan.scheduled]
    assert titles[0] == "high task"
    assert titles[1] == "med task"
    assert titles[2] == "low task"
    assert plan.total_scheduled_minutes == 30
    assert plan.skipped_tasks == []


def test_same_priority_shorter_task_first(ctx):
    owner, pet = ctx
    tasks = [
        Task("b", 20, "high"),
        Task("a", 10, "high"),
    ]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=60)
    assert [b.task.title for b in plan.scheduled] == ["a", "b"]


def test_budget_exhausts_lower_priority_first(ctx):
    owner, pet = ctx
    tasks = [
        Task("high", 40, "high"),
        Task("low", 40, "low"),
    ]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=50)
    assert len(plan.scheduled) == 1
    assert plan.scheduled[0].task.title == "high"
    assert len(plan.skipped_tasks) == 1
    assert plan.skipped_tasks[0][0].title == "low"


def test_task_longer_than_total_budget_skipped_with_reason(ctx):
    owner, pet = ctx
    tasks = [Task("impossible", 100, "high")]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=30)
    assert plan.scheduled == []
    assert len(plan.skipped_tasks) == 1
    assert "30" in plan.skipped_tasks[0][1]


def test_zero_budget_skips_all(ctx):
    owner, pet = ctx
    tasks = [Task("walk", 10, "high")]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=0)
    assert plan.scheduled == []
    assert len(plan.skipped_tasks) == 1
    assert "No time" in plan.skipped_tasks[0][1]


def test_scheduled_blocks_have_monotonic_start_times(ctx):
    owner, pet = ctx
    tasks = [
        Task("one", 15, "high"),
        Task("two", 15, "medium"),
    ]
    plan = build_daily_plan(owner, pet, tasks, available_minutes=60)
    assert plan.scheduled[0].start_minute == 0
    assert plan.scheduled[1].start_minute == 15
