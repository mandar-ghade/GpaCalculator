from dataclasses import dataclass
from enum import Enum
from pprint import pprint
from typing import Optional

class Grade(Enum):
    A = 'A'
    A_MINUS = 'A-'
    B_PLUS = 'B+'
    B = 'B'
    B_MINUS = 'B-'
    C_PLUS = 'C+'
    C = 'C'
    C_MINUS = 'C-'
    D_PLUS = 'D+'
    D = 'D'
    D_MINUS = 'D-'
    E = 'E'
    F = 'F'
    I_ = 'I'
    I_STAR = 'I*'


weights: dict[Grade, float] = {
    Grade.A: 4.0,
    Grade.A_MINUS: 3.67,
    Grade.B_PLUS: 3.33,
    Grade.B: 3.0,
    Grade.B_MINUS: 2.67,
    Grade.C_PLUS: 2.33,
    Grade.C: 2.0,
    Grade.C_MINUS: 1.67,
    Grade.D_PLUS: 1.33,
    Grade.D: 1.0,
    Grade.D_MINUS: 0.67,
    Grade.E: 0,
    Grade.F: 0,
    Grade.I_: 0,
    Grade.I_STAR: 0,
}


def parse_grade(grade_str: str) -> Optional[Grade]:
    try:
        return Grade(grade_str)
    except ValueError:
        return None


@dataclass
class Class:
    name: str # maybe an option for ID
    credits: int
    grade: Grade


@dataclass
class Semester:
    num: int
    classes: list[Class] # schedule


def get_grade_points(cls: Class) -> float:
    weight = weights.get(cls.grade, None)
    assert weight is not None, f'Grade for {cls.name} does not exist'
    return cls.credits * weight


def is_semester_line(line: str) -> bool:
    return len(line) >= 8 and line[0:8] == 'Semester'


def parse_class(line: str) -> Optional[Class]:
    args = line.split(' ')
    # case for invalid arguments or all spaces.
    if (len(args) <= 1 
        or line.isspace()
        or is_semester_line(line)):
        return None

    grade = parse_grade(args[0])
    if grade is None:
        return None
    credits = 0
    try:
        credits = int(args[1])
    except ValueError:
        return None
    class_name: str = ' '.join(args[2:]).strip()
    return Class(class_name, credits, grade)


def get_transcript(filename: str) -> list[Semester]:
    transcript: list[Semester] = []
    reader: list[str] = []
    with open(filename, 'r') as fp:
        reader = fp.readlines()
    i = 0
    while i < len(reader):
        line = reader[i]
        if not is_semester_line(line):
            i += 1
            continue
        # since int truncates leading 0s and whitespace
        semester_num: int = int(line[9:])
        # print(f'Semester: {semester_num}')
        classes: list[Class] = []
        while i + 1 < len(reader):
            cls = parse_class(reader[i+1])
            if cls is None:
                break
            classes.append(cls)
            i += 1
        semester: Semester = Semester(semester_num, classes)
        transcript.append(semester)
        i += 1
    return transcript


def calculate_gpa(transcript: list[Semester]) -> float:
    grade_points = 0
    credits = 0
    for schedule in transcript:
        for cls in schedule.classes:
            grade_points += get_grade_points(cls)
            credits += cls.credits
    return grade_points / credits


def main() -> None:
    transcript = get_transcript('transcript.txt')
    pprint(transcript)
    print(f"GPA: {calculate_gpa(transcript)}")


if __name__ == '__main__':
    main()
