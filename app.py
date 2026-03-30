import streamlit as st

from pawpal_system import Owner, Pet, Task, build_daily_plan

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan your pet's care for today using your available time and task priorities.")

with st.expander("About PawPal+", expanded=False):
    st.markdown(
        """
**PawPal+** helps you order care tasks (walks, feeding, meds, and more) for the time you
actually have. Tasks are sorted by **priority** (high first), then packed **greedily** into
your **daily minute budget** until no more tasks fit.
"""
    )

st.divider()

st.subheader("You and your pet")
col_o, col_p = st.columns(2)
with col_o:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_p:
    pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.subheader("Today's time budget")
available_minutes = st.number_input(
    "Minutes available for pet care today",
    min_value=0,
    max_value=24 * 60,
    value=120,
    step=15,
    help="The scheduler will not schedule more than this many minutes total.",
)

st.subheader("Tasks")
st.caption("Add care tasks with duration and priority. Remove mistakes with the controls below.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("**Current tasks**")
    st.dataframe(st.session_state.tasks, use_container_width=True, hide_index=True)

    remove_labels = [
        f"{i}: {t['title']} ({t['duration_minutes']} min, {t['priority']})"
        for i, t in enumerate(st.session_state.tasks)
    ]
    remove_options = ["(none)"] + remove_labels
    rm_col1, rm_col2 = st.columns([3, 1])
    with rm_col1:
        pick_remove = st.selectbox("Remove a task", remove_options)
    with rm_col2:
        st.write("")
        st.write("")
        if st.button("Remove") and pick_remove != "(none)":
            idx = int(pick_remove.split(":", 1)[0])
            st.session_state.tasks.pop(idx)
            st.rerun()
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build schedule")
gen = st.button("Generate schedule", type="primary")

if gen:
    owner = Owner(name=owner_name.strip() or "Owner")
    pet = Pet(name=pet_name.strip() or "Pet", species=species)
    task_models = [
        Task(
            title=t["title"],
            duration_minutes=int(t["duration_minutes"]),
            priority=t["priority"],
        )
        for t in st.session_state.tasks
    ]

    plan = build_daily_plan(owner, pet, task_models, int(available_minutes))

    st.success(
        f"Plan for **{plan.owner.name}** and **{plan.pet.name}** "
        f"({plan.pet.species}) — **{plan.total_scheduled_minutes}** / "
        f"**{plan.available_minutes}** minutes scheduled."
    )

    if not plan.scheduled and not st.session_state.tasks:
        st.info("Add at least one task to build a schedule.")
    elif plan.scheduled:
        rows = []
        for block in plan.scheduled:
            t = block.task
            rows.append(
                {
                    "Start (min)": block.start_minute,
                    "Task": t.title,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                    "Why scheduled": block.reason,
                }
            )
        st.markdown("**Scheduled blocks**")
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.warning("Nothing was scheduled. Check your time budget and task durations.")

    if plan.skipped_tasks:
        st.markdown("**Not included**")
        for task, reason in plan.skipped_tasks:
            st.caption(f"**{task.title}** ({task.duration_minutes} min, {task.priority}): {reason}")
