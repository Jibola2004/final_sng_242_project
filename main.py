import csv
from typing import Dict, List, Tuple, Optional
import re
from pprint import pprint

def is_valid_semester_format(semester: str) -> bool:
    return bool(re.fullmatch(r'\d{4}[123]', semester))

def translate_semester_type(semester: str) -> str:
    if len(semester) != 5 or not semester.isdigit():
        raise ValueError("Semester must be a 5-digit string like '20231'")
    
    year = int(semester[:4])
    point = int(semester[-1])
    
    if point == 1:
        return f'Fall {year}-{year + 1}'
    elif point == 2:
        return f'Spring {year}-{year + 1}'
    elif point == 3:
        return f'Summer {year}-{year + 1}'
    else:
        raise ValueError('Invalid semester code: should end in 1 (Fall), 2 (Spring), or 3 (Summer)')

class Course:
    course_details: Dict[int, 'Course'] = {}

    def __init__(self, numeric_course_code: int, course_code: str, course_name: str):
        self.numeric_course_code = numeric_course_code
        self.course_code = course_code
        self.course_name = course_name

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Course']:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        course = cls(
                            numeric_course_code=int(row['numeric_course_code']),
                            course_code=row['course_code'],
                            course_name=row['course_name']
                        )
                        cls.course_details[course.numeric_course_code] = course
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.course_details

class Curriculum:
    Curriculum_details: Dict[int, 'Curriculum'] = {}

    def __init__(self, numeric_course_code: int, credit: int, theory: int, 
                 practical: int, ects: float, prerequisite: List[int]):
        self.numeric_course_code = numeric_course_code
        self.credit = credit
        self.theory = theory
        self.practical = practical
        self.ects = ects
        self.prerequisite = prerequisite

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Curriculum']:
        cls.Curriculum_details.clear()
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        numeric_course_code = int(row['numeric_course_code'])
                        if numeric_course_code not in Course.course_details:
                            raise ValueError(f"Course {numeric_course_code} not found")
                        
                        prerequisite = []
                        prereq_str = row['prerequisite'].strip()
                        if prereq_str and prereq_str != 'Null':
                            try:
                                prerequisite = [int(code) for code in prereq_str.split('|')]
                            except ValueError:
                                raise ValueError(f"Invalid prerequisite format: {prereq_str}")

                        curriculum = cls(
                            numeric_course_code=numeric_course_code,
                            credit=int(row['credit']),
                            theory=int(row['theory']),
                            practical=int(row['practical']),
                            ects=float(row['ects']),
                            prerequisite=prerequisite
                        )
                        cls.Curriculum_details[numeric_course_code] = curriculum
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.Curriculum_details

class Department:
    department_details: Dict[int, 'Department'] = {}

    def __init__(self, dept_id: int, dept_name: str):
        self.dept_id = dept_id
        self.dept_name = dept_name

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Department']:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        department = cls(
                            dept_id=int(row['dept_id']),
                            dept_name=row['dept_name']
                        )
                        cls.department_details[department.dept_id] = department
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.department_details

class Student:
    student_details: Dict[int, 'Student'] = {}
    
    GRADE_POINTS = {
        'AA': 4.0,
        'BA': 3.5,
        'BB': 3.0,
        'CB': 2.5,
        'CC': 2.0,
        'DC': 1.5,
        'DD': 1.0,
        'FD': 0.5,
        'FF': 0.0,
        'NA': 0.0,
        'S': 0.0,
        "NS":0.0
    }

    def __init__(self, id: int, firstname: str, lastname: str, dept_id: int, year_of_entry: int):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.dept_id = dept_id
        self.entry_year = year_of_entry
        self.course_curriculum: Dict[int, 'Curriculum'] = {}
        self.courses_taken: Dict[str, List[Tuple[int, str]]] = {}
        self.total_credit_hour_taken: int = 0
        self.cgpa: float = 0.0
        self.total_credit_per_semester: Dict[str, int] = {}

    def fullname(self) -> str:
        return f'{self.lastname} {self.firstname}'

    def show_details(self):
        pprint(f'{self.lastname} {self.firstname}')
        pprint(self.courses_taken)

    @classmethod
    def from_csv(cls, file_path: str) -> Dict[int, 'Student']:
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        student = cls(
                            id=int(row['id']),
                            firstname=row['firstname'],
                            lastname=row['lastname'],
                            dept_id=int(row['dept_id']),
                            year_of_entry=int(row['year_of_entry'])
                        )
                        cls.student_details[student.id] = student
                    except (KeyError, ValueError) as e:
                        print(f"Error processing row {row}: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        return cls.student_details
    
    def load_course_curriculum(self) -> None:
        self.course_curriculum = {
            numeric_course_code: curriculum 
            for numeric_course_code, curriculum in Curriculum.Curriculum_details.items()
        }

    def update_credit_hours(self) -> None:
        self.total_credit_hour_taken = 0
        counted_courses = set()

        for _, courses in self.courses_taken.items():
            for numeric_code, _ in courses:
                if numeric_code not in counted_courses:
                    self.total_credit_hour_taken += int(self.course_curriculum[numeric_code].credit)
                    counted_courses.add(numeric_code)

    def calculate_cgpa(self) -> float:
        total_quality_points = 0.0
        total_credits = 0
        latest_grades = {}

        for semester in sorted(self.courses_taken.keys()):
            for numeric_course_code, grade in self.courses_taken[semester]:
                latest_grades[numeric_course_code] = grade

        for course_code, grade in latest_grades.items():
            if course_code not in self.course_curriculum:
                continue
            curriculum = self.course_curriculum[course_code]
            credit = curriculum.credit
            grade_point = self.GRADE_POINTS.get(grade.upper(), 0.0)
            total_quality_points += grade_point * credit
            total_credits += credit

        if total_credits == 0:
            return 0.0
        self.cgpa = round(total_quality_points / total_credits, 2)
        return self.cgpa

    def calculate_semester_gpa(self, semester: str) -> Optional[float]:
        if semester not in self.courses_taken or not self.courses_taken[semester]:
            return None

        total_quality_points = 0.0
        total_credits = 0

        for numeric_course_code, grade in self.courses_taken[semester]:
            if numeric_course_code not in self.course_curriculum:
                continue

            curriculum = self.course_curriculum[numeric_course_code]
            credit = curriculum.credit
            grade_point = self.GRADE_POINTS.get(grade.upper(), 0.0)

            total_quality_points += grade_point * credit
            total_credits += credit

        if total_credits == 0:
            return 0.0

        return round(total_quality_points / total_credits, 2)
    
    def add_course(self, semester: str, numeric_course_code: int, grade: str) -> None:
        try:
            if not is_valid_semester_format(semester):
                raise ValueError(f"Invalid semester format '{semester}'. Use 'YYYY1' for Fall or 'YYYY2' for Spring or 'YYYY3' for Summer.")
            if numeric_course_code not in self.course_curriculum:
                raise ValueError(f"Course {numeric_course_code} not found in curriculum")
            
            if grade.upper() not in self.GRADE_POINTS:
                raise ValueError(f"Invalid grade '{grade}'. Must be one of: {list(self.GRADE_POINTS.keys())}")
            
            if semester not in self.courses_taken:
                self.courses_taken[semester] = []
            
            for idx, (existing_code, _) in enumerate(self.courses_taken[semester]):
                if existing_code == numeric_course_code:
                    self.courses_taken[semester][idx] = (numeric_course_code, grade.upper())
                    break
            else:
                self.courses_taken[semester].append((numeric_course_code, grade.upper()))
            
            self.update_credit_hours()
            self.calculate_cgpa()
            
        except ValueError as e:
            print(f"Error adding course: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error adding course: {e}")
            raise

    def add_all_courses(self, data: Dict[str, List[Tuple[int, str]]]) -> None:
        try:
            for semester, courses in data.items():
                if not is_valid_semester_format(semester):
                    raise ValueError(f"Invalid semester format '{semester}' in batch data. Use 'YYYY1' or 'YYYY2'.")
                for numeric_course_code, grade in courses:
                    if numeric_course_code not in self.course_curriculum:
                        raise ValueError(f"Course {numeric_course_code} not found in curriculum")
                    if grade.upper() not in self.GRADE_POINTS:
                        raise ValueError(f"Invalid grade '{grade}' in semester '{semester}'.")

            self.courses_taken = data
            self.update_credit_hours()
            self.calculate_cgpa()

        except ValueError as e:
            print(f"Error adding courses: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error adding courses: {e}")
            raise
     
    def get_total_credit_per_semester(self):
        """Calculate and print total credits for each semester"""
        self.total_credit_per_semester = {}  # Clear previous data
        try:
            for semester, courses in self.courses_taken.items():
                semester_total = 0  # Reset for each semester
                for code, _ in courses:
                    semester_total += self.course_curriculum[code].credit
                self.total_credit_per_semester[semester] = semester_total
            print("Total credits per semester:")
            pprint(self.total_credit_per_semester)
            return self.total_credit_per_semester
        except KeyError as e:
            print(f"Error: Missing curriculum data for course {e}")
            raise
        except Exception as e:
            print(f"Error calculating semester credits: {e}")
            raise

    def generate_transcript_data(self):
        """Prepare transcript data structure"""
        if not self.total_credit_per_semester:
            self.get_total_credit_per_semester()
            
        transcript_data = {
            'student_name': self.fullname(),
            'student_id': self.id,
            'department': Department.department_details[self.dept_id].dept_name,
            'entry_year': self.entry_year,
            'cgpa': self.cgpa,
            'semesters': []
        }
    
        for semester in sorted(self.courses_taken.keys()):
            semester_data = {
                'name': translate_semester_type(semester),
                'total_credits': self.total_credit_per_semester.get(semester, 0),
                'gpa': self.calculate_semester_gpa(semester),
                'courses': []
            }
        
            for numeric_code, grade in self.courses_taken[semester]:
                course = Course.course_details[numeric_code]
                curriculum = Curriculum.Curriculum_details[numeric_code]
            
                semester_data['courses'].append({
                    'code': course.course_code,
                    'name': course.course_name,
                    'credit': curriculum.credit,
                    'grade': grade
                })
        
            transcript_data['semesters'].append(semester_data)

        return transcript_data

from data import data1

def main():
    # Load all data
    Department.from_csv('departments.csv')
    Course.from_csv('courses.csv')
    Curriculum.from_csv('cng_curriculum.csv')
    
    # Create and process student
    student = Student(2600724, 'Fathiu', 'Odetola', 355, 2012)
    student.load_course_curriculum()
    student.add_all_courses(data=data1)
    
    # Generate and display transcript data
    transcript = student.generate_transcript_data()
   
    return transcript

if __name__ == "__main__":
    main()