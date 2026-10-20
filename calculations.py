# calculations.py
# validation rules and the math behind them (credits, capacity, conflicts, stats)
# nothing in here touches files or windows
import re

DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# classes must fall between 7:00 AM and 10:00 PM, this also catches
# a wrong AM/PM (like 2:00 AM instead of 2:00 PM) when a course is added
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

# reads one time typed by a person and returns minutes after midnight, or None if it isn't valid
# "2:00 PM", "2pm", "2:30 p.m." are fine, and 24-hour times only from 13:00 on ("14:00")
# because "9:00" alone could be morning or evening
def read_clock(text):
    text = text.strip()
    m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*([ap])\.?m\.?", text, re.IGNORECASE)
    if m:
        h, mins = int(m.group(1)), int(m.group(2) or 0)
        if not 1 <= h <= 12 or mins > 59:
            return None
        pm = m.group(3).lower() == "p"
        return (h % 12 + (12 if pm else 0)) * 60 + mins
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", text)
    if m and 13 <= int(m.group(1)) <= 23 and int(m.group(2)) <= 59:
        return int(m.group(1)) * 60 + int(m.group(2))
    return None


# minutes after midnight -> "2:00 PM" (0 is 12:00 AM, 720 is 12:00 PM)
def format_clock(minutes):
    h, m = divmod(minutes, 60)
    return f"{h % 12 or 12}:{m:02d} {'PM' if h >= 12 else 'AM'}"


# "2:00 PM" -> 840, used on the times stored in courses.txt
# a plain hh:mm like "14:00" is also accepted in case someone edited the file by hand
def to_minutes(t):
    minutes = read_clock(t)
    if minutes is None:
        m = re.fullmatch(r"\s*(\d{1,2}):(\d{2})\s*", t)
        if not m or int(m.group(1)) > 23 or int(m.group(2)) > 59:
            raise ValueError(f"can't read the time {t!r}")
        minutes = int(m.group(1)) * 60 + int(m.group(2))
    return minutes


# "12:00 PM-2:00 PM" -> (start, end) in minutes
def parse_time(time_str):
    start_str, end_str = time_str.split('-')
    return to_minutes(start_str), to_minutes(end_str)


# " csai  101 " -> "CSAI 101" so the code matches however it was typed
def clean_code(code):
    return " ".join(code.upper().split())


# "sun, wed" -> "Sun,Wed" (the conflict check compares days as exact text)
def clean_days(days):
    return ",".join(d.strip().capitalize() for d in days.split(","))


# "9am - 11am" -> "9:00 AM-11:00 AM" (this is the format stored in courses.txt)
# anything that can't be read is returned as it is, and validate_course rejects it
def clean_time(time_str):
    parts = re.split(r"\s*[-–—]\s*", time_str.strip())
    if len(parts) == 2:
        start, end = read_clock(parts[0]), read_clock(parts[1])
        if start is not None and end is not None:
            return format_clock(start) + "-" + format_clock(end)
    return time_str.strip()


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

    # the time has to be what clean_time gives back, like "2:00 PM-4:00 PM"
    if not re.fullmatch(r"\d{1,2}:\d{2} [AP]M-\d{1,2}:\d{2} [AP]M", time_str):
        return False, "Time must look like 2:00 PM-4:00 PM (AM or PM on both sides)."
    start, end = parse_time(time_str)
    if start >= end:
        return False, "End time must be after start time (12:00 PM is noon, 12:00 AM is midnight)."
    if start < EARLIEST or end > LATEST:
        return False, "Classes must be between 7:00 AM and 10:00 PM. Check AM and PM."

    return True, "Valid course."


# True if this meeting overlaps one the student already has
def check_schedule_conflict(new_course, current_courses_details):
    new_days = [d.strip().capitalize() for d in new_course['days'].split(',')]
    try:
        new_start, new_end = parse_time(new_course['time'])
    except ValueError:
        return True, f"Can't read the time of {new_course['name']}, ask the admin to fix it."

    for course in current_courses_details:
        course_days = [d.strip().capitalize() for d in course['days'].split(',')]
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
