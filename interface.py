"""
Interface Module - Reda Mahmoud Ali (202507258)
This file has functions for searching, sorting, and displaying menus
We learned these in Lecture 07 (Algorithms) and Lecture 06 (Output)
"""

import calculations

def search_student_by_id(students, search_id):
    """Search for a student by ID"""
    for student in students:
        if student['id'] == search_id:
            return student
    return None


def search_student_by_name(students, search_name):
    """Search for a student by name"""
    results = []
    search_name = search_name.lower()
    
    for student in students:
        student_name = student['name'].lower()
        if search_name in student_name:
            results.append(student)
    
    return results


def search_course_by_code(courses, search_code):
    """Search for a course by code"""
    for course in courses:
        if course['code'] == search_code:
            return course
    return None


def sort_students_by_credits(students, registrations, courses):
    """Sort students by their credits using Bubble Sort"""
    student_credits = []
    
    for student in students:
        student_id = student['id']
        credits = calculations.calculate_total_credits(student_id, registrations, courses)
        student_credits.append({'student': student, 'credits': credits})
    
    n = len(student_credits)
    for i in range(n):
        for j in range(n - 1):
            if student_credits[j]['credits'] < student_credits[j + 1]['credits']:
                temp = student_credits[j]
                student_credits[j] = student_credits[j + 1]
                student_credits[j + 1] = temp
    
    return student_credits


def display_main_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print(" UNIVERSITY COURSE REGISTRATION SYSTEM")
    print("="*50)
    print("1. Login as Admin")
    print("2. Login as Student")
    print("0. Exit")
    print("="*50)


def display_admin_menu():
    """Display admin menu"""
    print("\n" + "="*50)
    print(" ADMIN MENU")
    print("="*50)
    print("1. View All Students")
    print("2. View All Courses")
    print("3. Search Student")
    print("4. Search Course")
    print("5. View Statistics")
    print("0. Logout")
    print("="*50)


def display_student_menu(student_name):
    """Display student menu"""
    print("\n" + "="*50)
    print(" STUDENT MENU - Welcome " + student_name + "!")
    print("="*50)
    print("1. View My Courses")
    print("2. Register New Course")
    print("3. Drop Course")
    print("0. Logout")
    print("="*50)


def check_login(username, password, students):
    """Check login credentials"""
    if username == "admin" and password == "admin123":
        return "admin"
    
    for student in students:
        if student['id'] == username and student['password'] == password:
            return student
    
    return None


def display_students(students):
    """Display all students in a nice format"""
    print("\n" + "-"*70)
    print("ID\t\tName\t\t\tProgram\tYear")
    print("-"*70)
    
    for student in students:
        print(f"{student['id']}\t{student['name']}\t\t{student['program']}\t{student['year']}")
    
    print("-"*70)


def display_courses(courses):
    """Display all courses"""
    print("\n" + "-"*80)
    print("Code\t\tName\t\t\t\tCredits\tDays\t\tTime")
    print("-"*80)
    
    for course in courses:
        print(f"{course['code']}\t{course['name']}\t{course['credits']}\t{course['days']}\t{course['time']}")
    
    print("-"*80)
