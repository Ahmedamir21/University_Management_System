"""
Main Program - Team Project
Team: Ahmed Amir, Ahmed Hisham, Reda Mahmoud
This is the main file that runs the whole program
"""

import file_operations
import calculations
import interface

def main():
    """Main function to run the program"""
    print("Starting University Registration System...")
    
    file_operations.initialize_files()
    
    students = file_operations.read_students()
    courses = file_operations.read_courses()
    registrations = file_operations.read_registrations()
    
    running = True
    while running:
        interface.display_main_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            result = interface.check_login(username, password, students)
            
            if result == "admin":
                print("Login successful! Welcome Admin.")
                admin_menu(students, courses, registrations)
            else:
                print("Login failed. Wrong username or password.")
        
        elif choice == "2":
            username = input("Student ID: ")
            password = input("Password: ")
            result = interface.check_login(username, password, students)
            
        if result is not None and result != "admin":                print("Login successful! Welcome " + result['name'])
                student_menu(result, students, courses, registrations)
            else:
                print("Login failed. Wrong ID or password.")
        
        elif choice == "0":
            print("Thank you for using the system. Goodbye!")
            running = False
        
        else:
            print("Invalid choice. Please try again.")


def admin_menu(students, courses, registrations):
    """Admin menu function"""
    admin_running = True
    while admin_running:
        interface.display_admin_menu()
        choice = input("Enter your choice: ")
        
        if choice == "1":
            interface.display_students(students)
        
        elif choice == "2":
            interface.display_courses(courses)
        
        elif choice == "3":
            search_id = input("Enter student ID to search: ")
            student = interface.search_student_by_id(students, search_id)
            if student:
                print("Found: " + student['name'])
            else:
                print("Student not found.")
        
        elif choice == "4":
            search_code = input("Enter course code: ")
            course = interface.search_course_by_code(courses, search_code)
            if course:
                print("Found: " + course['name'])
            else:
                print("Course not found.")
        
        elif choice == "5":
            stats = calculations.get_course_statistics(students, courses, registrations)
            print("\n=== STATISTICS ===")
            print("Total Students: " + str(stats['total_students']))
            print("Total Courses: " + str(stats['total_courses']))
            print("Total Registrations: " + str(stats['total_registrations']))
        
        elif choice == "0":
            admin_running = False
        
        else:
            print("Invalid choice.")


def student_menu(student, students, courses, registrations):
    """Student menu function"""
    student_running = True
    while student_running:
        interface.display_student_menu(student['name'])
        choice = input("Enter your choice: ")
        
        if choice == "1":
            print("\nYour registered courses:")
            for reg in registrations:
                if reg['student_id'] == student['id']:
                    course = interface.search_course_by_code(courses, reg['course_code'])
                    if course:
                        print("- " + course['name'])
        
        elif choice == "2":
            interface.display_courses(courses)
            course_code = input("Enter course code to register: ")
            
            course = interface.search_course_by_code(courses, course_code)
            if not course:
                print("Course not found.")
            else:
                is_duplicate = calculations.check_duplicate_registration(
                    student['id'], 
                    course_code, 
                    registrations
                )
                if is_duplicate:
                    print("You are already registered in this course.")
                else:
                    current_credits = calculations.calculate_total_credits(
                        student['id'], 
                        registrations, 
                        courses
                    )
                    can_register, message = calculations.check_credit_limit(
                        current_credits, 
                        course['credits']
                    )
                    print(message)
                    if can_register:
                        new_reg = {
                            'student_id': student['id'], 
                            'course_code': course_code
                        }
                        registrations.append(new_reg)
                        file_operations.write_registrations(registrations)
                        print("Successfully registered!")
        
        elif choice == "3":
            course_code = input("Enter course code to drop: ")
            found = False
            for reg in registrations:
                if reg['student_id'] == student['id'] and reg['course_code'] == course_code:
                    registrations.remove(reg)
                    file_operations.write_registrations(registrations)
                    print("Course dropped successfully.")
                    found = True
                    break
            if not found:
                print("You are not registered in this course.")
        
        elif choice == "0":
            student_running = False
        
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
