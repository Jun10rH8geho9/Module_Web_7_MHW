from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import create_engine

# Підключення до бази даних
engine = create_engine('postgresql://postgres:My5aK8_U91veR5ty@localhost:5432/fake_universaty')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    students_avg_grades = session.query(Student, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()
    print("Запит 1 виконано:")
    for student, avg_grade in students_avg_grades:
        print(f"Студент: {student.name}, Середній бал: {avg_grade}")
    print("\n")
    return students_avg_grades

def select_2(subject_name):
    # Знайти студента із найвищим середнім балом з певного предмета
    student_highest_avg_grade = session.query(Student, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade).join(Subject).filter(Subject.name == subject_name) \
        .group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()
    return student_highest_avg_grade

def select_3(subject_name):
    # Знайти середній бал у групах з певного предмета
    groups_avg_grade = session.query(Group.name, func.avg(Grade.grade).label('average_grade')) \
        .join(Student).join(Grade).join(Subject).filter(Subject.name == subject_name) \
        .group_by(Group.id).all()
    return groups_avg_grade

def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок)
    overall_avg_grade = session.query(func.avg(Grade.grade)).scalar()
    return overall_avg_grade

def select_5(teacher_name):
    # Знайти які курси читає певний викладач
    teacher_courses = session.query(Subject.name).join(Teacher).filter(Teacher.name == teacher_name).all()
    return teacher_courses

def select_6(group_name):
    # Знайти список студентів у певній групі
    group_students = session.query(Student.name).join(Group).filter(Group.name == group_name).all()
    return group_students

def select_7(group_name, subject_name):
    # Знайти оцінки студентів у окремій групі з певного предмета
    group_grades = session.query(Student.name, Grade.grade) \
        .join(Group).join(Grade).join(Subject) \
        .filter(Group.name == group_name, Subject.name == subject_name).all()
    return group_grades

def select_8(teacher_name):
    # Знайти середній бал, який ставить певний викладач зі своїх предметів
    teacher_avg_grade = session.query(func.avg(Grade.grade)) \
        .join(Subject).join(Teacher).filter(Teacher.name == teacher_name).scalar()
    return teacher_avg_grade

def select_9(student_name):
    # Знайти список курсів, які відвідує певний студент
    student_courses = session.query(Subject.name).join(Grade).join(Student) \
        .filter(Student.name == student_name).distinct().all()
    return student_courses

def select_10(student_name, teacher_name):
    # Список курсів, які певному студенту читає певний викладач
    student_teacher_courses = session.query(Subject.name) \
        .join(Grade).join(Student).join(Teacher) \
        .filter(Student.name == student_name, Teacher.name == teacher_name).distinct().all()
    return student_teacher_courses