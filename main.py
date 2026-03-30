"""CLI demo for PawPal+ — run: python main.py"""

from __future__ import annotations

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan")
    pet_mochi = Pet("Mochi", "dog")
    pet_luna = Pet("Luna", "cat")

    # Three tasks across two pets (titles show which pet each item is for)
    tasks = [
        Task(f"{pet_mochi.name}: morning walk", 25, "high"),
        Task(f"{pet_luna.name}: breakfast", 10, "high"),
        Task(f"{pet_mochi.name}: medication", 5, "medium"),
    ]

    scheduler = Scheduler()
    budget = 90
    plan = scheduler.build_daily_plan(owner, pet_mochi, tasks, available_minutes=budget)

    print(f"Owner: {owner.name}")
    print(
        f"Pets: {pet_mochi.name} ({pet_mochi.species}), "
        f"{pet_luna.name} ({pet_luna.species})"
    )
    print(f"Today's schedule ({budget} min budget)")
    print("-" * 44)

    if not plan.scheduled:
        print("  (nothing scheduled)")
    for block in plan.scheduled:
        t = block.task
        print(
            f"  {block.start_minute:3d} min  {t.title}  "
            f"({t.duration_minutes} min, {t.priority})"
        )
        print(f"           {block.reason}")

    if plan.skipped_tasks:
        print("\nNot included:")
        for task, reason in plan.skipped_tasks:
            print(f"  - {task.title}: {reason}")

    print(
        f"\nScheduled: {plan.total_scheduled_minutes} / "
        f"{plan.available_minutes} minutes"
    )


if __name__ == "__main__":
    main()
