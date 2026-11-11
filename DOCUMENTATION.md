# AI Planner — Project Documentation

## 1. Project overview

The AI Planner turns a goal into a practical task list and places estimated work into daily schedule blocks. It includes a Streamlit frontend and a terminal interface. Despite the project name, the delivered implementation uses local task templates and deterministic scheduling rules; it does not call a generative AI model or require an API key.

## 2. Objectives and features

- Suggest starter tasks for common project, study, and event goals.
- Allow the user to edit tasks and set a duration and priority.
- Schedule work within a daily time budget.
- Split long tasks across days and into manageable work blocks.
- Provide both a browser-based Streamlit interface and a terminal entry point.
- Keep the planning logic in a separate `main.py` module.

## 3. Project structure

```text
ai_planner/
├── app.py
├── main.py
├── requirements.txt
├── README.md
└── DOCUMENTATION.md
```

| File | Purpose |
|---|---|
| `main.py` | Defines task data, goal-based suggestions, line parsing, and scheduling. |
| `app.py` | Collects a goal, available time, start date, and editable tasks in Streamlit. |
| `requirements.txt` | Lists the Streamlit dependency. |
| `README.md` | Quick project summary and run instructions. |

## 4. Technology and architecture

- **Python 3.10+** implements the planner and date calculations.
- **Streamlit** provides the interactive web interface.
- **Dataclasses** represent tasks and scheduled work blocks.
- **Rule-based templates** suggest starter work from goal keywords.

```text
Goal + available minutes + start date
                 |
                 v
        suggest_tasks(goal)
                 |
                 v
      User edits task lines
  title | minutes | priority
                 |
                 v
     parse_task_lines(...)
                 |
                 v
       make_plan(tasks, ...)
                 |
                 v
         Dated work blocks
```

## 5. Installation and setup

1. Install Python 3.10 or later.
2. Open a terminal in the `ai_planner` folder.
3. Install the Streamlit dependency:

   ```powershell
   python -m pip install -r requirements.txt
   ```

   If Windows cannot find `python`, run the command with the full path to your installed interpreter. Example for the development computer:

   ```powershell
   & "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m pip install -r requirements.txt
   ```

4. Run the frontend:

   ```powershell
   python -m streamlit run app.py
   ```

   Or use the full interpreter path:

   ```powershell
   & "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m streamlit run app.py
   ```

5. Open the local URL printed by Streamlit, usually `http://localhost:8501`.

For the terminal interface, run `python main.py` in the project folder.

## 6. How to use the frontend

1. Enter a goal, for example `Build a portfolio website` or `Study for my biology exam`.
2. Set focused work time available each day.
3. Choose the schedule start date.
4. Review or edit the suggested task list.
5. Enter tasks one per line in this format:

   ```text
   Task title | minutes | priority
   ```

6. Select **Build my schedule** to see work blocks grouped by date.

Priority is `1` for high, `2` for normal, or `3` for low. If duration or priority is omitted, the parser uses 60 minutes and priority 2.

### Example task list

```text
Research three design options | 45 | 1
Build the first draft | 120 | 2
Review and polish | 60 | 3
```

With 120 minutes available each day, the planner schedules the high-priority task first and splits the 120-minute task into work blocks no longer than 90 minutes.

## 7. Scheduling behavior

`make_plan()` validates the available daily minutes, work-block duration, task durations, and priorities. Tasks are sorted by priority while retaining their original order within the same priority. Each task is assigned up to the remaining daily capacity and maximum block length. Remaining work continues on the following date.

The output is a date and duration for each work block. It does not assign a clock time, reserve calendar events, infer dependencies, or sync to an external calendar.

## 8. Goal templates

`suggest_tasks()` selects starter checklists using keywords for software/projects, study/exams, or events/trips. Goals that do not match those groups receive a general-purpose checklist. The user can edit all suggested lines in the frontend.

## 9. Dependencies

The planner logic uses Python's standard library. Streamlit is needed for the frontend and is listed in `requirements.txt`. No API key, model download, database, or network service is required.

## 10. Limitations and future improvements

- Suggestions are keyword-based templates rather than model-generated plans.
- The planner relies on the user's duration estimates and priority labels.
- It schedules by date and daily capacity only; it does not choose start/end clock times.
- It does not model task dependencies, weekends, holidays, reminders, or calendar availability.
- The terminal interface prints the suggested list but does not offer an interactive task editor.
- Future improvements could add dependencies, editable task tables, workday preferences, calendar export, and progress tracking.

## 11. Troubleshooting

- **`python` is not found:** Use your installed interpreter's full path as shown in setup.
- **`No module named streamlit`:** Install `requirements.txt` using the same Python interpreter that launches the app.
- **Invalid task line:** Use `Task title | minutes | priority`; minutes and priority must be whole numbers.
- **Priority error:** Enter only `1`, `2`, or `3`.
- **Duration error:** Use positive minutes. Daily capacity must be 15 to 720 minutes; work blocks must be at least 15 minutes and no longer than daily capacity.
- **No schedule appears:** Add at least one non-empty task line and select **Build my schedule**.

## 12. Manual usage checks

1. Enter a goal containing “project” and confirm a project checklist appears.
2. Change one task's duration and priority.
3. Build a schedule and confirm work is sorted by priority.
4. Give a task an estimate longer than one day's capacity and confirm it continues on a later date.
5. Try an invalid priority and confirm the interface shows a validation message.

## 13. Summary

The project demonstrates a local goal-to-schedule workflow with an editable Streamlit interface. The suggestions and schedule are deterministic and explainable, and require no cloud AI service.
