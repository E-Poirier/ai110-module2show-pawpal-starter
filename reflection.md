# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- The initial design separates **identity** (`Owner`, `Pet`) from **work items** (`Task`) and **results** (`DayPlan`, `ScheduledBlock`). Each `Task` has a title, duration in minutes, and a priority level (`low`, `medium`, `high`). The scheduler is a pure function `build_daily_plan(owner, pet, tasks, available_minutes)` that returns a `DayPlan` listing which tasks were placed on a simple minute timeline (`start_minute`) and why, plus any tasks that could not fit with explanations. See [uml.md](uml.md) for the class diagram.

**b. Design changes**

- Yes. I first imagined a richer “preferences” object on the owner; that was dropped for the first version so the only hard constraint is **minutes available today** plus **priority ordering**. Keeping preferences out of v1 made the scheduler easier to test and explain while still meeting the assignment’s core requirements.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler uses **total time available** (user-entered minutes for pet care today) and **per-task priority** (low / medium / high). Tasks are sorted by priority (highest first). Within the same priority, **shorter** tasks are scheduled before longer ones so more items can fit when time is tight. **Preferences** beyond priority are not modeled in code yet; species and names are only used for display in the plan summary.

**b. Tradeoffs**

- The main tradeoff is **greedy packing** versus globally optimal scheduling. The app picks tasks in priority order and adds them until the budget runs out; it does not search all subsets to maximize “value” or minimize gaps. That is reasonable for a daily pet-care checklist: owners usually want important tasks done first, not a perfect mathematical optimum, and the behavior is predictable and fast.

---

## 3. AI Collaboration

**a. How you used AI**

- AI was useful for structuring the project (package layout, test cases, and Streamlit wiring), and for drafting wording in this reflection. The most helpful prompts were ones that pointed at **constraints** (“respect a minute budget and priority”) and asked for **small, testable functions** instead of logic buried in the UI.

**b. Judgment and verification**

- I did not accept suggestions without running **`pytest`** and manually trying **Generate schedule** in Streamlit with edge cases (empty task list, zero minutes, one huge task). If a proposed behavior was unclear, I compared it to the rubric in the README (tasks, plan, explanations, tests) and adjusted the design to match what we could verify with tests.

---

## 4. Testing and Verification

**a. What you tested**

- Tests cover an **empty** task list, **all tasks fitting**, **priority order** when multiple tasks fit, **tie-breaking** (same priority: shorter task first), **budget exhaustion** (lower-priority task skipped), a task **longer than the whole budget**, **zero** available minutes, and **monotonic start times** on the timeline. These matter because they are the main ways the greedy scheduler can fail or surprise users.

**b. Confidence**

- I am fairly confident for the behaviors above because they are automated. With more time I would add tests for **duplicate task titles**, **very large task lists**, and **unicode** in titles to ensure the UI and scheduler stay robust.

---

## 5. Reflection

**a. What went well**

- Separating **`pawpal`** from **`app.py`** made the scheduler easy to test and kept the Streamlit file focused on input and display.

**b. What you would improve**

- A next iteration could add **owner preferences** (e.g. “walks only in the morning”) as constraints, or **recurring tasks**, and a smarter objective than pure greedy packing if the course allows.

**c. Key takeaway**

- Designing **data structures first** (`Task`, `DayPlan`) and a **pure scheduling function** paid off: the same logic runs in tests and in the UI without duplication.
