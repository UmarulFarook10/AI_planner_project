# AI Planner

A local Python planner that creates starter tasks from a goal, sorts them by priority, and places estimated work into daily blocks. It uses deterministic templates and scheduling rules; it does not call a cloud model or require an API key.

## How to enter tasks

Enter one task per line using:

```text
Task title | minutes | priority
```

Priority is `1` (high), `2` (normal), or `3` (low). Minutes and priority are optional; defaults are 60 minutes and priority 2.

Example:

```text
Research three design options | 45 | 1
Build the first draft | 120 | 2
Review and polish | 60 | 3
```

## Files

- `main.py` — task suggestions, task parsing, scheduling logic, and terminal interface.
- `app.py` — Streamlit web interface.
- `requirements.txt` — Streamlit dependency.
- `DOCUMENTATION.md` — fuller project, setup, scheduling, and usage guide.

## Run the Streamlit interface

Open a terminal in this folder, then run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If the `python` command opens the Microsoft Store or is not found, use your installed Python executable. For example, on the development computer used for this project:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe" -m streamlit run app.py
```

Open the local address printed by Streamlit, usually `http://localhost:8501`.

## Run the terminal interface

```powershell
python main.py
```

## Requirements

Python 3.10 or later. No API key, model download, database, or internet connection is required after Streamlit is installed.
