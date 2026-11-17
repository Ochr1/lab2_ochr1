# Lab 2: ALU Transcript Generator

A Python application and a Bash script that evaluate a student's grades and archive the grade data.

## Files
- `grade-evaluator.py` - reads `grades.csv`, validates it, and prints the transcript.
- `organizer.sh` - archives `grades.csv` with a timestamp and logs the action.
- `grades.csv` - the course grades (columns: `assignment,group,score,weight`).

## How to run the Python app
```
python grade-evaluator.py
```
Enter the CSV filename when asked (for example `grades.csv`).

What it does:
1. Checks every score is between 0 and 100.
2. Checks weights: total = 100, Summative = 40, Formative = 60.
3. Calculates the total grade and `GPA = (Total / 100) * 5.0`.
4. Passes the student only if both Formative and Summative are at least 50% (each measured against its own weight).
5. Lists the failed formative assignment(s) with the highest weight as eligible for resubmission, including ties.

No external libraries are used; only built-in Python.

## How to run the organizer
```
bash organizer.sh
```
It creates `archive/` if needed, moves `grades.csv` to `archive/grades_YYYYMMDD-HHMMSS.csv`, creates a new empty `grades.csv`, and appends a line to `organizer.log`.

## Error handling
Missing file, empty file, missing columns, non-numeric values, out-of-range scores and wrong weights all print a clear message instead of crashing.
