from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Student, Group, Teacher, Subject, Grade
import random
from datetime import datetime, timedelta


# Підключення до бази даних
engine = create_engine('postgresql://postgres:My5aK8_U91veR5ty@localhost:5432/fake_universaty')
Base.metadata.bind = engine

# Створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# Ініціалізація Faker
fake = Faker()

def create_students(groups):
    students = []
    for _ in range(30, 51):
        student = Student(name=fake.name(), group_id=random.choice(groups).id)
        students.append(student)
        session.add(student)
        session.commit()
    return students

def create_groups():
    groups = [Group(name=f'Group {i}') for i in range(1, 4)]
    session.add_all(groups)
    session.commit()
    return groups

def create_teachers():
    teachers = [Teacher(name=fake.name()) for _ in range(3)]
    session.add_all(teachers)
    session.commit()
    return teachers

def create_subjects(teachers):
    subjects = []
    for _ in range(5, 9):
        teacher = random.choice(teachers)
        subject = Subject(name=fake.word(), teacher_id=teacher.id)
        subjects.append(subject)
    session.add_all(subjects)
    session.commit()
    return subjects


def create_grades(students, subjects):
    for student in students:
        for subject in subjects:
            for _ in range(random.randint(1, 5)):
                grade = Grade(student_id=student.id, subject_id=subject.id, grade=random.randint(60, 100),
                              date=fake.date_between(start_date='-1y', end_date='today'))
                session.add(grade)
    session.commit()

def main():
    groups = create_groups()
    teachers = create_teachers()
    subjects = create_subjects(teachers)
    students = create_students(groups)
    create_grades(students, subjects)
    print("Дані успішно додані до бази даних.")

if __name__ == "__main__":
    main()