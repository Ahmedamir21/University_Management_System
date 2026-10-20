# file_operations.py
# reads and writes the text files inside data/ (one line = one record, fields split by "|")
#
#   students.txt       id | name | program | year | password
#   courses.txt        code | name | credits | days | time | capacity
#   registrations.txt  student_id | course_code
#   applications.txt   id | name | email | phone | status
#   notifications.txt  application_id | message | status
#
# the other files never open these directly, they use the read_/write_ functions below
# which work with lists of dicts
import os
import re

import calculations

# ----- settings -----

# data folder lives next to the code
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
SEP = "|"  # not "," because names/days can contain commas

STUDENTS_FILE = "students.txt"
COURSES_FILE = "courses.txt"
REGISTRATIONS_FILE = "registrations.txt"
APPLICATIONS_FILE = "applications.txt"
NOTIFICATIONS_FILE = "notifications.txt"
TIME_FORMAT_FILE = "time_format.txt"  # marker: says how the times in courses.txt are stored


# ----- core helpers -----

def _path(name):
    return os.path.join(DATA_DIR, name)


# returns every line as a list of fields
# missing file -> empty list, broken lines are skipped
# so one bad line doesn't crash the app
#
def _read(name, min_fields):
    rows = []
    if os.path.exists(_path(name)):
        with open(_path(name), "r", encoding="utf-8-sig") as f:  # -sig: ignores the BOM Notepad can add
            for line in f:
                fields = line.strip().split(SEP)
                if len(fields) >= min_fields:
                    rows.append(fields)
    return rows


# save rows to a data file
# write to a .tmp file first and then replace the real one, so a
# crash while saving can't leave a half-written file
#
def _write(name, rows):
    tmp = _path(name) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for row in rows:
            # user text can't contain the separator or newlines
            f.write(SEP.join(str(v).replace(SEP, "/").replace("\n", " ") for v in row) + "\n")
    os.replace(tmp, _path(name))


# int() that doesn't crash on bad values
def _to_int(text, default=0):
    try:
        return int(text)
    except ValueError:
        return default


# ----- students -----

def read_students():
    return [{'id': p[0], 'name': p[1], 'prog': p[2], 'year': p[3], 'pass': p[4]}
            for p in _read(STUDENTS_FILE, 5)]


def write_students(students):
    _write(STUDENTS_FILE, [[s['id'], s['name'], s['prog'], s['year'], s['pass']] for s in students])


# ----- courses -----

def read_courses():
    return [{'code': p[0], 'name': p[1], 'cred': _to_int(p[2]), 'days': p[3],
             'time': p[4], 'capacity': _to_int(p[5])}
            for p in _read(COURSES_FILE, 6)]


def write_courses(courses):
    _write(COURSES_FILE, [[c['code'], c['name'], c['cred'], c['days'], c['time'], c['capacity']]
                          for c in courses])


# ----- registrations -----

def read_registrations():
    return [{'student_id': p[0], 'course_code': p[1]} for p in _read(REGISTRATIONS_FILE, 2)]


def write_registrations(regs):
    _write(REGISTRATIONS_FILE, [[r['student_id'], r['course_code']] for r in regs])


# True if the registration existed and was removed
def drop_course(std_id, course_code):
    regs = read_registrations()
    new_regs = [r for r in regs if not (r['student_id'] == std_id and r['course_code'] == course_code)]
    if len(regs) != len(new_regs):
        write_registrations(new_regs)
        return True
    return False


# ----- applications -----

def read_applications():
    return [{'id': p[0], 'name': p[1], 'email': p[2], 'phone': p[3], 'status': p[4]}
            for p in _read(APPLICATIONS_FILE, 5)]


def write_applications(apps):
    _write(APPLICATIONS_FILE, [[a['id'], a['name'], a['email'], a['phone'], a['status']] for a in apps])


# new applications start as Pending, ids start at 1001
def submit_application(name, email, phone):
    apps = read_applications()
    ids = [int(a['id']) for a in apps if a['id'].isdigit()]
    new_id = str(max(ids) + 1 if ids else 1001)
    apps.append({'id': new_id, 'name': name, 'email': email, 'phone': phone, 'status': 'Pending'})
    write_applications(apps)
    return new_id


def notify_applicant(app_id, msg):
    with open(_path(NOTIFICATIONS_FILE), "a", encoding="utf-8") as f:
        f.write(f"{app_id}{SEP}{msg}{SEP}New\n")


# ----- old time formats -----

# earlier versions of the project stored times in other ways:
#   - the first one had no am/pm and read hours 1 to 7 as afternoon ("2:00-4:00" meant 2 PM to 4 PM)
#   - the second one used 24-hour times ("14:00-16:00") and wrote "24h" in time_format.txt
# this reads one stored time (like "2:00" or "14:00") and returns minutes after midnight
def _part_to_minutes(part, is_24h):
    m = re.fullmatch(r"(\d{1,2}):(\d{2})\s*([AaPp][Mm])?", part.strip())
    if not m:
        raise ValueError(part)
    h, mins, suffix = int(m.group(1)), int(m.group(2)), m.group(3)
    if mins > 59:
        raise ValueError(part)
    if suffix:
        if not 1 <= h <= 12:
            raise ValueError(part)
        h = h % 12 + (12 if suffix.lower() == "pm" else 0)
    else:
        if not is_24h and h < 8:
            h += 12
        if h > 23:
            raise ValueError(part)
    return h * 60 + mins


# data files made by an older version are converted once, then the marker file says "ampm"
def _convert_old_times():
    if not os.path.exists(_path(COURSES_FILE)):
        return
    marker = ""
    if os.path.exists(_path(TIME_FORMAT_FILE)):
        with open(_path(TIME_FORMAT_FILE), "r", encoding="utf-8") as f:
            marker = f.read().strip()
    if marker == "ampm":
        return

    courses = read_courses()
    for c in courses:
        try:
            start, end = [_part_to_minutes(p, marker == "24h") for p in c['time'].split("-")]
        except ValueError:
            continue  # not in an old format, leave it
        if start < end:  # an end before the start can't be converted, leave it
            c['time'] = calculations.format_clock(start) + "-" + calculations.format_clock(end)
    write_courses(courses)


# ----- first-run setup -----

# create data/ and any missing file with starter data so
# the app doesn't crash on first run (existing files are kept)
#
def initialize_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    _convert_old_times()

    if not os.path.exists(_path(STUDENTS_FILE)):
        write_students([
            {'id': '202507440', 'name': 'Ahmed Amir Ibrahim', 'prog': 'CS', 'year': '2025', 'pass': 'pass123'},
            {'id': '202506915', 'name': 'Ahmed Hisham Saad', 'prog': 'CS', 'year': '2025', 'pass': 'pass456'},
            {'id': '202507258', 'name': 'Reda Mahmoud Ali', 'prog': 'CS', 'year': '2025', 'pass': 'pass789'},
        ])

    if not os.path.exists(_path(COURSES_FILE)):
        # rows with the same code are one course (lecture + lab, Sec1 + Sec2),
        # registering the code registers all of them
        write_courses([
            {'code': 'CSAI 100', 'name': 'Introduction to Computational Sciences and AI', 'cred': 1, 'days': 'Sun', 'time': '3:00 PM-4:00 PM', 'capacity': 50},
            {'code': 'CSAI 101', 'name': 'Fundamentals of Programming and Computer Science', 'cred': 2, 'days': 'Wed', 'time': '12:00 PM-2:00 PM', 'capacity': 50},
            {'code': 'CSAI 101', 'name': 'Fundamentals of Programming and Computer Science Lab', 'cred': 0, 'days': 'Thu', 'time': '8:00 AM-10:00 AM', 'capacity': 50},
            {'code': 'CSAI 102', 'name': 'Digital Logic and Computer Architecture', 'cred': 3, 'days': 'Tue', 'time': '2:00 PM-4:00 PM', 'capacity': 50},
            {'code': 'CSAI 102', 'name': 'Digital Logic and Computer Architecture Lab', 'cred': 0, 'days': 'Mon', 'time': '10:00 AM-12:00 PM', 'capacity': 50},
            {'code': 'CSAI 252', 'name': 'Introduction to Computer Networks', 'cred': 3, 'days': 'Wed', 'time': '2:00 PM-4:00 PM', 'capacity': 50},
            {'code': 'CSAI 252', 'name': 'Introduction to Computer Networks Lab', 'cred': 0, 'days': 'Mon', 'time': '12:00 PM-2:00 PM', 'capacity': 50},
            {'code': 'ENGL 002', 'name': 'Remedial English Sec1', 'cred': 0, 'days': 'Sun', 'time': '1:00 PM-3:00 PM', 'capacity': 50},
            {'code': 'ENGL 002', 'name': 'Remedial English Sec2', 'cred': 0, 'days': 'Thu', 'time': '10:00 AM-12:00 PM', 'capacity': 50},
            {'code': 'ENGL 003', 'name': 'Remedial English Sec1', 'cred': 0, 'days': 'Sun', 'time': '1:00 PM-3:00 PM', 'capacity': 50},
            {'code': 'ENGL 003', 'name': 'Remedial English Sec2', 'cred': 0, 'days': 'Thu', 'time': '10:00 AM-12:00 PM', 'capacity': 50},
            {'code': 'ENGL 004', 'name': 'Remedial English Sec1', 'cred': 0, 'days': 'Sun', 'time': '1:00 PM-3:00 PM', 'capacity': 50},
            {'code': 'ENGL 004', 'name': 'Remedial English Sec2', 'cred': 0, 'days': 'Thu', 'time': '10:00 AM-12:00 PM', 'capacity': 50},
            {'code': 'MATH 103', 'name': 'Calculus for Computational Sciences', 'cred': 3, 'days': 'Sun', 'time': '8:00 AM-10:00 AM', 'capacity': 50},
            {'code': 'MATH 103', 'name': 'Calculus for Computational Sciences Tut1', 'cred': 0, 'days': 'Tue', 'time': '12:00 PM-2:00 PM', 'capacity': 50},
            {'code': 'MATH 103', 'name': 'Calculus for Computational Sciences Tut2', 'cred': 0, 'days': 'Wed', 'time': '10:00 AM-12:00 PM', 'capacity': 50},
            {'code': 'SCH 163', 'name': 'Sustainability Social and Ethical Issues in Computing', 'cred': 2, 'days': 'Tue', 'time': '8:00 AM-10:00 AM', 'capacity': 50},
        ])

    if not os.path.exists(_path(REGISTRATIONS_FILE)):
        write_registrations([
            {'student_id': '202507440', 'course_code': 'CSAI 101'},
            {'student_id': '202507440', 'course_code': 'MATH 103'},
            {'student_id': '202506915', 'course_code': 'CSAI 101'},
        ])

    for name in (APPLICATIONS_FILE, NOTIFICATIONS_FILE):
        if not os.path.exists(_path(name)):
            open(_path(name), "w", encoding="utf-8").close()

    # from here on the times in courses.txt are like "2:00 PM-4:00 PM"
    with open(_path(TIME_FORMAT_FILE), "w", encoding="utf-8") as f:
        f.write("ampm\n")
