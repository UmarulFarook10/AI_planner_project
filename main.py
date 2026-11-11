from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, timedelta
from typing import Iterable


@dataclass
class PlanTask:
    title: str
    minutes: int = 60
    priority: int = 2  # 1 = high, 3 = low


@dataclass
class WorkBlock:
    date: date
    title: str
    minutes: int
    priority: int


def suggest_tasks(goal: str) -> list[PlanTask]:
    """Make a practical starter checklist from common project types."""
    text = goal.casefold()
    if any(word in text for word in ("app", "software", "website", "project", "program")):
        titles = [
            "Define the goal, audience, and success criteria",
            "List requirements and choose the smallest useful scope",
            "Sketch the design and plan the main components",
            "Build the core feature",
            "Review the result and fix gaps",
            "Prepare a short demo and final notes",
        ]
    elif any(word in text for word in ("exam", "study", "learn", "course")):
        titles = [
            "List topics and identify the hardest areas",
            "Study the first topic and make concise notes",
            "Study the remaining topics",
            "Practice with questions or a mock exam",
            "Review mistakes and revisit weak areas",
        ]
    elif any(word in text for word in ("event", "party", "conference", "trip")):
        titles = [
            "Set the date, budget, and guest or traveler needs",
            "Compare and book the key venue or transport",
            "Arrange food, materials, and other essentials",
            "Confirm plans with everyone involved",
            "Check the final itinerary and prepare a backup plan",
        ]
    else:
        titles = [
            "Clarify the outcome and what done means",
            "Break the work into small, concrete steps",
            "Complete the first high-value step",
            "Continue the remaining work",
            "Review, finish, and share the result",
        ]
    return [PlanTask(title, minutes=60, priority=1 if i < 2 else 2) for i, title in enumerate(titles)]


def make_plan(
    tasks: Iterable[PlanTask],
    daily_minutes: int = 120,
    start_date: date | None = None,
    max_block_minutes: int = 90,
) -> list[WorkBlock]:
    """Schedule tasks by priority, splitting long tasks across available days."""
    if not 15 <= daily_minutes <= 720:
        raise ValueError("Available time must be between 15 and 720 minutes per day.")
    if not 15 <= max_block_minutes <= daily_minutes:
        raise ValueError("Block length must be at least 15 minutes and no longer than daily time.")
    items = list(tasks)
    if any(task.minutes <= 0 for task in items):
        raise ValueError("Every task must take at least 1 minute.")
    if any(task.priority not in (1, 2, 3) for task in items):
        raise ValueError("Priority must be 1 (high), 2 (normal), or 3 (low).")

    # Stable sort keeps the user's order when priorities match.
    items.sort(key=lambda task: task.priority)
    first_day = start_date or date.today()
    blocks: list[WorkBlock] = []
    day_offset = 0
    remaining_today = daily_minutes
    for task in items:
        remaining_task = task.minutes
        while remaining_task:
            if remaining_today <= 0:
                day_offset += 1
                remaining_today = daily_minutes
            amount = min(remaining_task, remaining_today, max_block_minutes)
            blocks.append(
                WorkBlock(first_day + timedelta(days=day_offset), task.title, amount, task.priority)
            )
            remaining_task -= amount
            remaining_today -= amount
    return blocks


def parse_task_lines(raw: str) -> list[PlanTask]:
    """Parse one task per line: title | minutes | priority (the last two are optional)."""
    tasks: list[PlanTask] = []
    for line_number, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [part.strip() for part in line.split("|")]
        try:
            minutes = int(parts[1]) if len(parts) > 1 and parts[1] else 60
            priority = int(parts[2]) if len(parts) > 2 and parts[2] else 2
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: minutes and priority must be whole numbers.") from exc
        if not parts[0]:
            raise ValueError(f"Line {line_number}: task title cannot be blank.")
        tasks.append(PlanTask(parts[0], minutes, priority))
    return tasks


def plan_to_dicts(blocks: Iterable[WorkBlock]) -> list[dict[str, str | int]]:
    return [{**asdict(block), "date": block.date.isoformat()} for block in blocks]


def main() -> None:
    goal = input("What do you want to accomplish? ").strip()
    tasks = suggest_tasks(goal)
    print("\nSuggested tasks:")
    for index, task in enumerate(tasks, 1):
        print(f"{index}. {task.title} ({task.minutes} min, priority {task.priority})")
    raw_capacity = input("Minutes available per day [120]: ").strip()
    capacity = int(raw_capacity) if raw_capacity else 120
    blocks = make_plan(tasks, daily_minutes=capacity)
    print("\nSchedule:")
    for block in blocks:
        print(f"{block.date:%a %d %b}: {block.title} — {block.minutes} min")


if __name__ == "__main__":
    main()
