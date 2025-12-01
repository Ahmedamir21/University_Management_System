"""
Calculations Module - Ahmed Hisham Saad (202506915)
Responsible for calculations, validations, and statistics.
Uses concepts from Lectures 01-05: Arithmetic, if-else, Loops, Nested conditions
"""

import file_operations

def calculate_total_credits(student_id, registrations, courses):
    """Calculate total credit hours for a student"""
    total = 0
    for reg in registrations:
        if reg['student_id'] == student_id:
            for course in courses:
                if course['code'] == reg['course_code']:
                    total = total + course['credits']
    return total


def check_credit_limit(current_credits, new_credits):
    """Check if adding new course exceeds credit limits (12-18)"""
    total = current_credits + new_credits
    
    if total > 18:
        return (False, f"Cannot register. Total would be {total}, exceeding maximum 18 credits.")
    elif total < 12:
        return (True, f"Warning: Total will be {total} credits (below recommended 12).")
    else:
        return (True, f"Registration allowed. Total will be {total} credits.")


def check_duplicate_registration(student_id, course_code, registrations):
    """Check if student already registered for this course"""
    for reg in registrations:
        if reg['student_id'] == student_id and reg['course_code'] == course_code:
            return True
    return False


def count_students_per_course(registrations, courses):
    """Count how many students registered in each course"""
    counts = {}
    
    for course in courses:
        counts[course['code']] = 0
    
    for reg in registrations:
        course_code = reg['course_code']
        if course_code in counts:
            counts[course_code] = counts[course_code] + 1
    
    return counts


def get_course_statistics(students, courses, registrations):
    """Get comprehensive statistics about the system"""
    stats = {}
    
    stats['total_students'] = len(students)
    stats['total_courses'] = len(courses)
    stats['total_registrations'] = len(registrations)
    
    if len(students) > 0:
        stats['avg_courses'] = len(registrations) / len(students)
    else:
        stats['avg_courses'] = 0
    
    course_counts = count_students_per_course(registrations, courses)
    
    if course_counts:
        max_count = 0
        min_count = 9999
        most_popular = ""
        least_popular = ""
        
        for code in course_counts:
            count = course_counts[code]
            if count > max_count:
                max_count = count
                most_popular = code
            if count < min_count:
                min_count = count
                least_popular = code
        
        stats['most_popular'] = most_popular
        stats['most_popular_count'] = max_count
        stats['least_popular'] = least_popular
        stats['least_popular_count'] = min_count
    
    fulltime = 0
    parttime = 0
    
    for student in students:
        credits = calculate_total_credits(student['id'], registrations, courses)
        if credits >= 12:
            fulltime = fulltime + 1
        elif credits > 0:
            parttime = parttime + 1
    
    stats['fulltime_students'] = fulltime
    stats['parttime_students'] = parttime
    
    return stats


def check_schedule_conflict(student_id, new_course_code, registrations, courses):
    """Check if new course conflicts with student's current schedule"""
    new_course = None
    for course in courses:
        if course['code'] == new_course_code:
            new_course = course
            break
    
    if not new_course:
        return (False, "Course not found")
    
    new_days = new_course['days']
    new_time = new_course['time']
    
    for reg in registrations:
        if reg['student_id'] == student_id:
            for course in courses:
                if course['code'] == reg['course_code']:
                    if course['days'] == new_days:
                        if course['time'] == new_time:
                            return (True, f"Schedule conflict with {course['code']} on {course['days']} at {course['time']}")
    
    return (False, "No schedule conflict")


if __name__ == "__main__":
    print("Testing calculations.py...")
    file_operations.initialize_files()
    
    students = file_operations.read_students()
    courses = file_operations.read_courses()
    registrations = file_operations.read_registrations()
    
    if students:
        student_id = students[0]['id']
        credits = calculate_total_credits(student_id, registrations, courses)
        print(f"\nStudent {student_id} has {credits} credits")
    
    stats = get_course_statistics(students, courses, registrations)
    print(f"\nStatistics:")
    print(f"Total Students: {stats['total_students']}")
    print(f"Total Courses: {stats['total_courses']}")
    print(f"Total Registrations: {stats['total_registrations']}")
