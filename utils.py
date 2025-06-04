import re
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


def isValidStudent_id(student_id:str)->bool:
     return bool(re.fullmatch(r'\d{7}', student_id))