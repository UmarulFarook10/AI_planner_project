from datetime import date

import streamlit as st

from main import PlanTask, make_plan, parse_task_lines, suggest_tasks


st.set_page_config(page_title="AI Planner", page_icon="🗓️", layout="wide")
st.title("🗓️ AI Planner")
st.caption("Builds a useful schedule from your goal and task estimates")

goal = st.text_input("Your goal", placeholder="Build a portfolio website")
left, right = st.columns(2)
with left:
    capacity = st.slider("Focused work time per day (minutes)", min_value=30, max_value=480, value=120, step=15)
with right:
    start = st.date_input("Start date", value=date.today())

suggested = suggest_tasks(goal) if goal else []
default_lines = "\n".join(f"{task.title} | {task.minutes} | {task.priority}" for task in suggested)
raw = st.text_area(
    "Tasks — one per line: title | minutes | priority (1 high, 2 normal, 3 low)",
    value=default_lines,
    height=240,
    key=f"task_editor_{goal}",
    placeholder="Research options | 45 | 1\nWrite first draft | 90 | 2",
)

if st.button("Build my schedule", type="primary"):
    try:
        tasks = parse_task_lines(raw)
        if not tasks:
            st.warning("Add at least one task to build a schedule.")
        else:
            blocks = make_plan(tasks, daily_minutes=capacity, start_date=start)
            st.subheader("Your schedule")
            for day in sorted({block.date for block in blocks}):
                with st.container(border=True):
                    st.markdown(f"**{day.strftime('%A, %B %d')}**")
                    for block in (item for item in blocks if item.date == day):
                        st.write(f"• {block.title} — {block.minutes} min")
            total = sum(block.minutes for block in blocks)
            st.caption(f"{len(blocks)} work blocks · {total // 60} hr {total % 60} min total")
    except ValueError as exc:
        st.error(str(exc))
