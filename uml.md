# PawPal+ UML (class diagram)

This diagram matches the implementation in the `pawpal` package.

```mermaid
classDiagram
    class Owner {
        +str name
    }
    class Pet {
        +str name
        +str species
    }
    class Task {
        +str title
        +int duration_minutes
        +str priority
    }
    class ScheduledBlock {
        +Task task
        +int start_minute
        +str reason
    }
    class DayPlan {
        +Owner owner
        +Pet pet
        +int available_minutes
        +list scheduled
        +list skipped_tasks
        +total_scheduled_minutes() int
    }
    class build_daily_plan {
        <<function>>
        +build_daily_plan(Owner, Pet, list~Task~, int) DayPlan
    }

    Owner "1" -- "1" DayPlan : context
    Pet "1" -- "1" DayPlan : context
    Task "1" -- "*" ScheduledBlock
    DayPlan *-- "*" ScheduledBlock : scheduled
    DayPlan ..> build_daily_plan : creates
```

**Responsibilities**

- **Owner** / **Pet**: Hold basic identity for the plan header and context.
- **Task**: One care item with duration and priority (`low` / `medium` / `high`).
- **ScheduledBlock**: A chosen task placed at `start_minute` with a short explanation.
- **DayPlan**: Full result: what fit in the time budget, what was skipped, and totals.
- **build_daily_plan**: Pure scheduling function—sorts by priority, packs greedily into `available_minutes`, and builds reasons.
