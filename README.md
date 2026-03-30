# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Project layout (CodePath Unit 5)

| Piece | Role |
|-------|------|
| [`pawpal_system.py`](pawpal_system.py) | Logic-layer entry point: re-exports models + `build_daily_plan`, and a `Scheduler` class |
| [`pawpal/`](pawpal/) | Implementation (`models`, `scheduler`) |
| [`app.py`](app.py) | Streamlit UI (imports from `pawpal_system`) |
| [`main.py`](main.py) | CLI demo: `python main.py` |
| [`tests/test_pawpal.py`](tests/test_pawpal.py) | Tests via `pawpal_system` |
| [`tests/test_scheduler.py`](tests/test_scheduler.py) | Same behaviors, direct `pawpal` imports |

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run CLI demo

```bash
python main.py
```

### Run tests

```bash
python -m pytest
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
