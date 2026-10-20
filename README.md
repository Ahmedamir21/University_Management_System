# University Management System

A desktop app written in Python (Tkinter) that handles university admissions and course registration. We built it as a team of three for CSAI 101 (Fundamentals of Programming and Computer Science), Fall 2025.

Before this, applications and registration were done by hand, which means mistakes like double-booked schedules or students going over the credit limit. The app does those checks automatically.

## Features

- Applicants fill in a form and the admin accepts or rejects them. An accepted applicant gets a student ID.
- Students log in to see all courses, register, drop and view their schedule.
- Registration is checked for the 18 credit-hour limit, course capacity, duplicate registration and time conflicts.
- A course code covers all of its meetings, so registering a course also registers its lab (or both English sections).
- The admin can view students and courses, add courses, see enrollment numbers and open a bar chart of students per course.
- Course codes are not case sensitive when registering or dropping (`csai 101` works). When the admin adds a course, the days and the time are checked first, so a wrong time can't break the conflict check later.

## Running it

You need Python 3 with Tkinter. The installer from python.org already includes it. On Linux you may need `sudo apt install python3-tk`.

```
git clone https://github.com/Ahmedamir21/University_Management_System
cd University_Management_System
pip install -r requirements.txt
python main.py
```

On Windows use `py main.py` if `python` is not recognized.

Demo logins: `admin` / `admin`, or a student like `202507440` / `pass123`.

The `data/` folder with the text files is created automatically the first time the app runs, and it is in `.gitignore`. To reset the app to the starter data, close it and delete the `data/` folder.

When adding a course, days are written like `Sun` or `Mon,Wed` and the time like `2:00 PM-4:00 PM` (`2pm-4pm` also works). Classes have to be between 7:00 AM and 10:00 PM. A `data/` folder made by an older version (times without AM/PM) is converted automatically the first time the app starts.

## Project structure

| File | What it does |
| --- | --- |
| `main.py` | The Tkinter windows. Start the app from here |
| `calculations.py` | Rules and validation (credits, capacity, time conflicts, statistics) |
| `file_operations.py` | Reads and writes the text files in `data/` |
| `interface.py` | Search and sort helpers, report, and the Matplotlib chart |

Data is stored in plain text files (`students.txt`, `courses.txt`, `registrations.txt`, `applications.txt`), one record per line with fields separated by `|`.

## Team

| Name | Part |
| --- | --- |
| Ahmed Amir Ibrahim | Data and files |
| Ahmed Hisham Saad | Logic and validation |
| Reda Mahmoud Ali | Interface (search, sort, report, chart) |

## Things we ran into

- Our first version stored times like `12:00-2:00` with no AM/PM, so it had to guess that hours 1 to 7 were afternoon. Now every time has AM or PM (`12:00 PM-2:00 PM`), and it is converted to minutes before checking overlaps.
- The GUI only calls functions from `calculations.py` and `file_operations.py`, so the logic stays separate from the windows.
- Each of us worked on a separate file and `main.py` joins them together.

## Limitations and ideas

- Passwords are stored as plain text, which is fine for a course project but not for real use. A newly accepted student gets the default password `123456`.
- Search and sort are console functions in `interface.py` and are not in the GUI yet.
- Next steps: move to a real SQL database, add a tuition payment module, and export reports to PDF or Excel.
