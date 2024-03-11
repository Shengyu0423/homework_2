class Student:
    def __init__(self, first_name, last_name, class_name):
        self.first_name = first_name
        self.last_name = last_name
        self.class_name = class_name

class Teacher:
    def __init__(self, first_name, last_name, class_name):
        self.first_name = first_name
        self.last_name = last_name
        self.class_name = class_name

class HomeroomTeacher:
    def __init__(self, first_name, last_name, class_name):
        self.first_name = first_name
        self.last_name = last_name
        self.class_name = class_name

database = {
    "students": [
        {"first_name": "John", "last_name": "Smith", "class": "3C"},
        {"first_name": "Anna", "last_name": "Purple", "class": "3C"},
        {"first_name": "Jan", "last_name": "Kowalski", "class": "4E"},
    ],
    "teachers": [
        {"first_name": "Jason", "last_name": "Statham", "subject": "math", "classes": ["3C", "4E"]},
    ],
    "homeroom_teachers": [
        {"first_name": "Jan", "last_name": "Kowalski", "class": "3C"},
    ]
}

while True:
    print("\nHello! Welcome to Future School Management Software system!")
    print("\nPlease input one of following commands: create, manage, end.")
    command = input("\nEnter a command: ").lower()

    if command == "create":
        print("\nPlease choose one of categories that you want to create: student, teacher, homeroom teacher, end.")
        category = input("\nEnter a category: ").lower()
        if category == "student":
            print("\nPlease provide the following information of the student: ")
            first_name = input("\nEnter the first name of the student: ")
            last_name = input("\nEnter the last name of the student: ")
            class_name = input("\nEnter the class name: ")

            # Add new student to database
            new_student = {"first_name": first_name, "last_name": last_name, "class": class_name}
            database["students"].append(new_student)
            print("\nCreate the new student successfully!")
        elif category == "teacher":
            print("\nPlease provide the following information of the teacher: ")
            first_name = input("\nEnter the first name of the teacher: ")
            last_name = input("\nEnter the last name of the teacher: ")
            subject = input("\nEnter the subject of the teacher teaches: ")
                   
            # The class(es) that new teacher teach
            classes_taught = []
            while True:
                class_name = input("\nEnter the class name of the teacher teaches (press enter to finish): ")
                if class_name == "":
                    break
                classes_taught.append(class_name)

            # Add new teacher to database
            new_teacher = {"first_name": first_name, "last_name": last_name, "subject": subject, "classes": classes_taught}
            database["teachers"].append(new_teacher)
            print("\nCreate the new teacher successfully!")
        elif category == "homeroom teacher":
            print("\nPlease provide the following information of the homeroom teacher: ")
            first_name = input("\nEnter the first name of the homeroom teacher: ")
            last_name = input("\nEnter the last name of the homeroom teacher: ")
            class_name = input("\nEnter the class name of the homeroom teacher leads: ")

            # Add new homeroom teacher to database
            new_homeroom_teacher = {"first_name": first_name, "last_name": last_name, "class": class_name}
            database["homeroom_teachers"].append(new_homeroom_teacher)
            print("\nCreate the new homeroom teacher successfully!")
        elif category == "end":
            print("\nReurn to the main menu.")
            continue
        else:
            print("\nError: Invalid category for choosing!")     

    elif command == "manage":
        print("\nPlease choose one of categories that you want to manage: class, student, teacher, homeroom teacher, end.")
        category = input("\nEnter a category: ").lower()
        if category == "class":
            while True:
                class_number = input("\nPlease input the class number: ")

                # check if the class number exists in the database
                class_exists = any("class" in student and student["class"] == class_number for student in database["students"]) or any("class" in teacher and teacher["class"] == class_number for teacher in database["teachers"])

                if class_exists:
                    break
                else:
                    print("\nError: Class not found in the database. Please enter a valid class number.")
                
            students_in_class = [student for student in database["students"] if student["class"] == class_number]
            print("\nStudents in class", class_number)
            for student in students_in_class:
                print(f"{student["first_name"]} {student["last_name"]}")

            homeroom_teacher = next((teacher for teacher in database["homeroom_teachers"] if teacher["class"] == class_number), None)
            if homeroom_teacher:
                print(f"\nHomeroom teacher for class {class_number}: {homeroom_teacher["first_name"]} {homeroom_teacher["last_name"]}")
            else:
                print("\nNo homeroom teacher assigned for class", class_number)
        
        elif category == "student":
            print("\nPlease provide the following information of the student: ")
            first_name = input("\nEnter the first name of the student: ")
            last_name = input("\nEnter the last name of the sudent: ")
            for student in database["students"]:
                if student["first_name"] == first_name and student["last_name"] == last_name:
                    print(f"\nStudent: {first_name} {last_name} attends class {student["class"]}")
                    for teacher in database["teachers"]:
                        if student["class"] in teacher["classes"]:
                            print(f"Teacher for this class: {teacher["first_name"]} {teacher["last_name"]}")
                    break
            else:
                print("\nError: Student is not in the database!")

        elif category == "teacher":
            print("\nPlease provide the following information of the teacher: ")
            first_name = input("\nEnter the first name of the teacher: ")
            last_name = input("\nEnter the last name of the teacher: ")
            for teacher in database["teachers"]:
                if teacher["first_name"] == first_name and teacher["last_name"] == last_name:
                    print(f"\nTeacher: {first_name} {last_name} teaches class {teacher["classes"]}")
                    break
            else:
                print("\nError: Teacher is not in the database!")

        elif category == "homeroom teacher":
            print("\nPlease provide the following information of the homeroom teacher: ")
            first_name = input("\nEnter the first name of the homeroom teacher: ")
            last_name = input("\nEnter the last name of the homeroom teacher: ")
            for homeroom_teacher in database["homeroom_teachers"]:
                if homeroom_teacher["first_name"] == first_name and homeroom_teacher["last_name"] == last_name:
                    print(f"\nHomeroom teacher: {first_name} {last_name} leads class {homeroom_teacher["class"]}")
                    print("\nStudent's list: ") 
                    for student in database["students"]:
                        if student["class"] == homeroom_teacher["class"]:
                            print(f"{student["first_name"]} {student["last_name"]}")
                    break
            else:
                print("\nError: Homeroom teacher is not in the database!")

        elif category == "end":
            print("\nReturn to the main menu.")
            continue            
        else:
            print("\nError: Invalid category for choosing!")
    elif command == "end":
         print("\nGoodbye! Have a nice day!")
         break
    else:
         print("\nError: Please enter a valid command!")

                          

                     









