<div align="center">

# 🎓 University Management System (UMS)
### A Python-Based Academic Management Application with GUI

**Course:** CSCI 101 — Introduction to Computer Science · Fall 2025
**Team:** Team 1

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-orange?style=flat-square)

</div>

---

## 📌 Overview

**University Management System (UMS)** is a Python application built to replace manual, error-prone university admissions and course registration processes with a **unified, automated system**. It features a full **Tkinter GUI**, persistent file-based data storage, and real-time academic rule validation — built collaboratively by a 3-person team as a course project.

---

## 🎯 Problem It Solves

University admissions and registration are traditionally handled manually or through disjointed systems, leading to:

- ❌ **Human error** — approving schedule conflicts or exceeding credit limits by mistake
- 🐌 **Inefficiency** — slow processing of applications and ID generation
- 🕳️ **Lack of visibility** — no easy way for admins to track course popularity or student distribution

**Goal:** Build a unified, automated, and error-free system for both students and administrators.

---

## ✨ Core Objectives

- **Automate Admissions** — auto-generate student IDs and profiles upon acceptance
- **Enforce Academic Rules** — validate credit hours (12–18) and prerequisites in real time
- **Prevent Conflicts** — algorithmically detect time overlaps in student schedules
- **Enhance Usability** — provide a visual dashboard for both students and admins

---

## 🏗️ System Architecture

The system follows a **modular design** with 3 interconnected modules integrated by a main controller:

| Module | Responsibility |
|---|---|
| **File Operations** | Handles data persistence — reading/writing `.txt` files |
| **Calculations** | Business logic layer — validation rules and conflict-detection algorithms |
| **Interface** | Manages user interaction flow and visualization |
| **Main Controller** | Integrates all modules into a single GUI application |

---

## 👥 Team & Contributions

| Member | Student ID | Area of Responsibility |
|---|---|---|
| **Ahmed Amir Ibrahim** | 202507440 | Data & Files (database layer) |
| Ahmed Hisham Saad | 202506915 | Logic & Validation |
| Reda Mahmoud Ali | 202507258 | User Interface & Experience |

### 🔹 Data & Files — Ahmed Amir Ibrahim
- Used formatted text files (`students.txt`, `courses.txt`, `registrations.txt`) to simulate a database.
- Implemented robust File I/O functions ensuring data is saved permanently and persists across program sessions.
- **Key feature:** automatic file initialization (`initialize_files`) to prevent crashes when data files are missing.

### 🔹 Logic & Validation — Ahmed Hisham Saad
- **Credit check:** `check_credit_limit` ensures total credits stay ≤ 18.
- **Conflict detection:** `check_schedule_conflict` parses time strings (e.g. `"Sun 3:00-4:00"`) and compares them mathematically to prevent overlaps.
- **Capacity check:** prevents registration once `current_students >= course_capacity`.

### 🔹 User Interface & Experience — Reda Mahmoud Ali
- **Search & sort** algorithms to find students/courses and sort by popularity or credits.
- **Reporting** logic to generate enrollment statistics for the admin dashboard.
- **Menu structure** with a clear separation between "Student Mode" and "Admin Mode".

---

## 🎁 Bonus Features (Collective Team Effort)

The team went beyond the core requirements to deliver a more polished experience:

- **GUI Implementation (Tkinter):** replaced the command-line interface with a full windowed application (buttons, tables, pop-ups).
- **Data Visualization (Matplotlib):** integrated charts showing "Students per Course" to support admin decision-making.

> **Why:** to make the system user-friendly and visually appealing for non-technical users.

---

## 🧩 Challenges & Solutions

| Challenge | Solution |
|---|---|
| Parsing time strings (e.g. `"12:00-2:00"`) to detect overlaps | Converted times to minutes-from-midnight integers for straightforward comparison |
| Connecting the GUI to backend logic without freezing the app | Clean separation of concerns — the GUI calls functions from `calculations.py` only when buttons are pressed |
| Managing team code integration | Strict modularity — each member worked on a separate file, joined together via `main.py` |

---

## 🎬 Demo Walkthrough

1. **Admin:** Log in → accept a "Pending" applicant → system auto-generates a student ID (`2025...`).
2. **Admin:** Add a new course (e.g. "AI 101").
3. **Student:** Log in with the new ID → register for "AI 101".
4. **Validation:** Attempt to register for a conflicting course → error pop-up is shown.
5. **Bonus:** Click "Show Chart" to see the enrollment bar graph update in real time.

---

## 🚀 Future Roadmap

- 🗄️ Integration with a real SQL database
- 💰 A "Finance Module" for tuition payments
- 📄 Exporting reports to PDF/Excel

---

## 📂 Repository Contents

| File | Description |
|---|---|
| `UMS__From_Pain_to_Python.pptx` | Final project presentation deck |
| `main.py` *(if included)* | Main controller integrating all modules into the GUI app |
| `calculations.py` *(if included)* | Business logic — validation & conflict-detection algorithms |
| `file_operations.py` *(if included)* | Data persistence layer (`students.txt`, `courses.txt`, `registrations.txt`) |
| `interface.py` *(if included)* | GUI and user interaction flow |

> ⚠️ **Note:** the source code files above are listed based on the architecture described in the project presentation. Since the actual final source files haven't been confirmed yet, file names are marked as placeholders — update this table once the final codebase is finalized.

---

<div align="center">

**Course:** CSCI 101 — Introduction to Computer Science · Fall 2025

</div>
