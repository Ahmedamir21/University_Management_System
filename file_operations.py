"""
File Operations Module - Ahmed Amir Ibrahim (202507440)
Responsible for reading and writing data to files.
Uses concepts from Lectures 01-03: Variables, Lists, Strings, File I/O
"""

def read_students():
    """
    Read student data from students.txt file.
    Returns: List of dictionaries containing student information
    """
    students = []
    try:
        file = open("data/students.txt", "r")
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",")
                student = {
                    'id': parts[0],
                    'name': parts[1],
                    'program': parts[2],
                    'year': parts[3],
                    'password': parts[4]
                }
                students.append(student)
        file.close()
    except FileNotFoundError:
        print("Warning: students.txt not found. Starting with empty list.")
    return students


def write_students(students):
    """
    Write student data to students.txt file.
    Parameters: students - List of student dictionaries
    """
    file = open("data/students.txt", "w")
    for student in students:
        line = f"{student['id']},{student['name']},{student['program']},{student['year']},{student['password']}\n"
        file.write(line)
    file.close()
    print("Students data saved successfully.")


def read_courses():
    """
    Read course data from courses.txt file.
    Returns: List of dictionaries containing course information
    """
    courses = []
    try:
        file = open("data/courses.txt", "r")
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",")
                course = {
                    'code': parts[0],
                    'name': parts[1],
                    'credits': int(parts[2]),
                    'days': parts[3],
                    'time': parts[4]
                }
                courses.append(course)
        file.close()
    except FileNotFoundError:
        print("Warning: courses.txt not found. Starting with empty list.")
    return courses


def write_courses(courses):
    """
    Write course data to courses.txt file.
    Parameters: courses - List of course dictionaries
    """
    file = open("data/courses.txt", "w")
    for course in courses:
        line = f"{course['code']},{course['name']},{course['credits']},{course['days']},{course['time']}\n"
        file.write(line)
    file.close()
    print("Courses data saved successfully.")


def read_registrations():
    """
    Read registration data from registrations.txt file.
    Returns: List of dictionaries containing registration information
    """
    registrations = []
    try:
        file = open("data/registrations.txt", "r")
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(",")
                registration = {
                    'student_id': parts[0],
                    'course_code': parts[1]
                }
                registrations.append(registration)
        file.close()
    except FileNotFoundError:
        print("Warning: registrations.txt not found. Starting with empty list.")
    return registrations


def write_registrations(registrations):
    """
    Write registration data to registrations.txt file.
    Parameters: registrations - List of registration dictionaries
    """
    file = open("data/registrations.txt", "w")
    for reg in registrations:
        line = f"{reg['student_id']},{reg['course_code']}\n"
        file.write(line)
    file.close()
    print("Registrations data saved successfully.")


def initialize_files():
    """
    Create data files if they don't exist and add sample data.
    This function is called when the program starts for the first time.
    """
    try:
        import os
        if not os.path.exists("data"):
            os.makedirs("data")
            print("Data directory created.")
    except:
        pass
    
    try:
        file = open("data/students.txt", "r")
        file.close()
    except FileNotFoundError:
        file = open("data/students.txt", "w")
        file.write("202507440,Ahmed Amir,CS,2025,pass123\n")
        file.write("202506915,Ahmed Hisham,CS,2025,pass456\n")
        file.write("202507258,Reda Mahmoud,CS,2025,pass789\n")
        file.close()
        print("students.txt created with sample data.")
    
    try:
        file = open("data/courses.txt", "r")
        file.close()
    except FileNotFoundError:
        file = open("data/courses.txt", "w")
        file.write("CS101,Introduction to Programming,3,Sun-Tue,10:00-11:30\n")
        file.write("CS102,Data Structures,3,Mon-Wed,12:00-13:30\n")
        file.write("MATH101,Calculus I,4,Sun-Tue,14:00-16:00\n")
        file.write("PHYS101,Physics I,4,Mon-Wed,08:00-10:00\n")
        file.close()
        print("courses.txt created with sample data.")
    
    try:
        file = open("data/registrations.txt", "r")
        file.close()
    except FileNotFoundError:
        file = open("data/registrations.txt", "w")
        file.write("202507440,CS101\n")
        file.write("202507440,MATH101\n")
        file.write("202506915,CS101\n")
        file.close()
        print("registrations.txt created with sample data.")


if __name__ == "__main__":
    print("Testing file_operations.py...")
    initialize_files()
    
    students = read_students()
    print(f"\nLoaded {len(students)} students")
    
    courses = read_courses()
    print(f"Loaded {len(courses)} courses")
    
    registrations = read_registrations()
    print(f"Loaded {len(registrations)} registrations")
