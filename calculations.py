# calculations.py
# validation rules and the math behind them (credits, capacity, conflicts, stats)
# nothing in here touches files or windows
import re

DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# classes must fall between 07:00 and 22:00, this also catches
# someone typing 12-hour times like 2:00-4:00 by mistake
EARLIEST = 7 * 60
LATEST = 22 * 60


# ----- credits -----

# sum of credits for the courses the student registered in
def calculate_total_credits(student_registrations, all_courses):
    total = 0
    for reg in student_registrations:
        for course in all_courses:
            if course['code'] == reg['course_code']:
                total += course['cred']
    return total


# max is 18 credit hours
def check_credit_limit(current_total, new_course_credits):
    if current_total + new_course_credits > 18:
        return False, "Error: Credit hours exceeded 18."
    return True, "Valid credit hours."


# ----- registration checks -----

# can't register the same course twice
def check_duplicate_registration(student_id, course_code, registrations):
    for reg in registrations:
        if reg['student_id'] == student_id and reg['course_code'] == course_code:
            return True, "Student already registered."
    return False, "Course available."


# is there still room in the course?
def check_course_capacity(course_code, all_courses, all_registrations):
    capacity = 0
    for course in all_courses:
        if course['code'] == course_code:
            capacity = course['capacity']
            break

    current_count = 0
    for reg in all_registrations:
        if reg['course_code'] == course_code:
            current_count += 1

    if current_count >= capacity:
        return False, "Error: Course is full."
    return True, "Seats available."


# ----- schedule conflicts -----

# hh:mm (24-hour time) -> minutes after midnight, 14:00 = 840
def to_minutes(t):
    h, m = map(int, t.split(':'))
    return h * 60 + m


# "12:00-2:00" -> (start, end) in minutes
def parse_time(time_str):
    start_str, end_str = time_str.split('-')
    return to_minutes(start_str), to_minutes(end_str)


# " csai  101 " -> "CSAI 101" so the code matches however it was typed
def clean_code(code):
    return " ".join(code.upper().split())


# "sun, wed" -> "Sun,Wed" (the conflict check compares days as exact text)
def clean_days(days):
    return ",".join(d.strip().capitalize() for d in days.split(","))


# "9:00 - 11:00" -> "09:00-11:00" (all times are stored as hh:mm-hh:mm)
def clean_time(time_str):
    time_str = time_str.replace(" ", "")
    if re.fullmatch(r"\d{1,2}:\d{2}-\d{1,2}:\d{2}", time_str):
        return "-".join(p.zfill(5) for p in time_str.split("-"))
    return time_str


# checks a course before the admin saves it, because a bad time or day
# would break the conflict check for every student later
def validate_course(code, name, cred, days, time_str, capacity):
    if not code or not name:
        return False, "Code and name are required."
    if cred < 0:
        return False, "Credits can't be negative."
    if capacity < 1:
        return False, "Capacity must be at least 1."

    for d in clean_days(days).split(","):
        if d not in DAYS:
            return False, "Days must look like Sun or Mon,Wed."

    if not re.fullmatch(r"\d{1,2}:\d{2}-\d{1,2}:\d{2}", time_str):
        return False, "Time must look like 14:00-16:00 (24-hour)."
    for part in time_str.split("-"):
        h, m = map(int, part.split(":"))
        if h > 23 or m > 59:
            return False, "Time is not valid."
    start, end = parse_time(time_str)
    if start >= end:
        return False, "End time must be after start time."
    if start < EARLIEST or end > LATEST:
        return False, "Use 24-hour time between 07:00 and 22:00, like 14:00-16:00."

    return True, "Valid course."


# True if this meeting overlaps one the student already has
def check_schedule_conflict(new_course, current_courses_details):
    new_days = new_course['days'].split(',')
    new_start, new_end = parse_time(new_course['time'])

    for course in current_courses_details:
        course_days = course['days'].split(',')
        common_days = [day for day in new_days if day in course_days]
        if common_days:
            try:
                curr_start, curr_end = parse_time(course['time'])
            except ValueError:
                continue  # a broken time in the data file shouldn't crash registration
            if max(new_start, curr_start) < min(new_end, curr_end):
                return True, f"Conflict with {course['name']}"
    return False, "No conflict."


# all the registration checks in one place
# one code can have several meetings (lecture + lab, Sec1 + Sec2)
# and they are registered together, so every meeting gets checked
def validate_registration(student_id, code, regs, courses):
    meetings = [x for x in courses if x['code'] == code]
    if not meetings:
        return False, "Course not found."

    mine = [r for r in regs if r['student_id'] == student_id]

    dup, msg = check_duplicate_registration(student_id, code, mine)
    if dup:
        return False, msg

    ok, msg = check_course_capacity(code, courses, regs)
    if not ok:
        return False, msg

    new_credits = sum(m['cred'] for m in meetings)
    ok, msg = check_credit_limit(calculate_total_credits(mine, courses), new_credits)
    if not ok:
        return False, msg

    my_codes = [r['course_code'] for r in mine]
    registered = [x for x in courses if x['code'] in my_codes]
    for m in meetings:
        conflict, msg = check_schedule_conflict(m, registered)
        if conflict:
            return False, msg

    return True, "OK"


# ----- statistics -----

# students per course
def count_students_per_course(all_registrations):
    counts = {}
    for reg in all_registrations:
        code = reg['course_code']
        counts[code] = counts.get(code, 0) + 1
    return counts


# returns (most popular code, count, least popular code, count)
def get_course_statistics(student_counts_dict):
    if not student_counts_dict:
        return None, 0, None, 0

    first = list(student_counts_dict.keys())[0]
    max_c, max_v = first, student_counts_dict[first]
    min_c, min_v = first, student_counts_dict[first]

    for k, v in student_counts_dict.items():
        if v > max_v:
            max_c, max_v = k, v
        if v < min_v:
            min_c, min_v = k, v
    return max_c, max_v, min_c, min_v


# ----- applications -----

# basic checks on the application form
def validate_application(name, email, phone):
    if not name or not email or not phone:
        return False, "Missing fields."
    if "@" not in email:
        return False, "Invalid email."
    if not phone.isdigit() or len(phone) < 10:
        return False, "Invalid phone."
    return True, "Valid application."


# status of an application by its id
def track_application_status(app_id, applications):
    for app in applications:
        if app['id'] == app_id:
            return app['status']
    return "Not Found"


# ----- students -----

# make sure the id isn't taken
def add_student(student_data, all_students):
    for s in all_students:
        if s['id'] == student_data['id']:
            return False, "ID exists."
    return True, "Valid student."


# not used yet, the real checks are in validate_registration
def register_student_in_course(student_id, course_code, all_registrations):
    return True, "Ready to register."
