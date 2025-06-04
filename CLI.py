from main import Student,Department,Course,Curriculum
import random
from data import data_cng_1,data_cng_4,data_cyg_1,data_cyg_2,sng_data_1
from utils import isValidStudent_id
# load department,students and course details
Department.from_csv('departments.csv')
Course.from_csv('courses.csv')
Student.from_csv('students.csv')



CURRICULUM_VALUE={
    389:'SNG_CURRICULUM_1.csv', #Software Engineering
    355:'cng_curriculum.csv',   #Computer Engineering
    390:'cyg_curriculum.csv',  #CyberSecurity Engineering
}

"""
print('\nWelcome to METU Transcript Generator')
print('''
      1. Show all the list Students\n
      2. Show all the Department list \n
      3. Download Student Transcript using student id \n
      4. Download all Student Transcript in a Department \n
      ''')
choice=input('Enter your choice: ')

if   choice == '1':
    Student.show_full_student_details()
elif choice == '2':
    Department.show_all_department()
elif choice == '3':
    
    student_id=input('Enter your student id: ')
    if not isValidStudent_id(student_id=student_id):
        raise ValueError('student id is not vaild.') 
    student_id_int=int(student_id)
    if student_id_int not in Student.student_details.keys():
        raise ValueError('Student not found in Student details.') 
    
    student=Student.student_details[student_id_int]
    dept_id=student.dept_id

    
    Curriculum.from_csv(CURRICULUM_VALUE[dept_id])
    student.load_course_curriculum()

    if dept_id == 355:
        cng_data=random.choice([data_cng_1,data_cng_4])
        student.add_all_courses(data=cng_data)
    elif dept_id == 390:
        cyg_data=random.choice([data_cyg_1,data_cyg_2]) 
        student.add_all_courses(data=cyg_data) 
    elif dept_id == 389:
        student.add_all_courses(data=sng_data_1) 


    # Generate and display transcript data
    transcript = student.generate_transcript_data()
    # Generate transcript data html
    student.generate_transcript_html(transcript_data=transcript)
elif choice == '4':
    print('''
       Department ID,Department Name\n   
       355-Computer Engineering\n
       389-Software Engineering\n
       390-CyberSecurity Engineering\n
      ''')
    department_id=input('Enter department id: ')
    department_id_int =int(department_id)
    if department_id_int not in Department.department_details.keys():
        raise ValueError('Department id not found in Department details.') 
    for student_id, student_obj in Student.student_details.items():
         if department_id_int == student_obj.dept_id:
             student=Student.student_details[student_id]
             dept_id=student.dept_id

    
             Curriculum.from_csv(CURRICULUM_VALUE[dept_id])
             student.load_course_curriculum()

             if dept_id == 355:
                cng_data=random.choice([data_cng_1,data_cng_4])
                student.add_all_courses(data=cng_data)
             elif dept_id == 390:
                cyg_data=random.choice([data_cyg_1,data_cyg_2]) 
                student.add_all_courses(data=cyg_data) 
             elif dept_id == 389:
                student.add_all_courses(data=sng_data_1)
                 # Generate and display transcript data
             transcript = student.generate_transcript_data()
              # Generate transcript data html
             student.generate_transcript_html(transcript_data=transcript)   
elif choice == 'exit':
    pass
"""


def generate_and_download_transcript(student):
    dept_id = student.dept_id
    Curriculum.from_csv(CURRICULUM_VALUE[dept_id])
    student.load_course_curriculum()

    if dept_id == 355:
        student.add_all_courses(data=random.choice([data_cng_1, data_cng_4]))
    elif dept_id == 390:
        student.add_all_courses(data=random.choice([data_cyg_1, data_cyg_2]))
    elif dept_id == 389:
        student.add_all_courses(data=sng_data_1)

    transcript = student.generate_transcript_data()
    student.generate_transcript_html(transcript_data=transcript)

while True:
    print('\nWelcome to METU Transcript Generator')
    print('''
1. Show all the list of Students
2. Show all the Department list
3. Download Student Transcript using Student ID
4. Download all Student Transcripts in a Department
Type "exit" to quit.
''')

    choice = input('Enter your choice: ').strip()

    if choice == '1':
        Student.show_full_student_details()

    elif choice == '2':
        Department.show_all_department()

    elif choice == '3':
        student_id = input('Enter your student id: ')
        
        if not isValidStudent_id(student_id=student_id):
            print('❌ Student ID is not valid.')
            continue

        student_id_int = int(student_id)
        
        if student_id_int not in Student.student_details:
            print('❌ Student not found in Student details.')
            continue

        student = Student.student_details[student_id_int]
        generate_and_download_transcript(student)

    elif choice == '4':
        print('''
Department ID - Department Name
355 - Computer Engineering
389 - Software Engineering
390 - CyberSecurity Engineering
''')
        department_id = input('Enter department id: ').strip()
        
        if not department_id.isdigit():
            print("❌ Department ID must be numeric.")
            continue

        department_id_int = int(department_id)

        if department_id_int not in Department.department_details:
            print('❌ Department ID not found in Department details.')
            continue

        for student_id, student in Student.student_details.items():
            if student.dept_id == department_id_int:
                generate_and_download_transcript(student)

    elif choice.lower() == 'exit':
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid choice. Please try again.")

             





    

    
          





