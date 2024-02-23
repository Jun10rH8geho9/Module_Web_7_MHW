from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
from sqlalchemy import create_engine
import random

# Підключення до бази даних
engine = create_engine('postgresql://postgres:My5aK8_U91veR5ty@localhost:5432/fake_universaty')
Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    students_avg_grades = session.query(Student, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()
    return students_avg_grades

def select_2(subject_name):
    # Знайти студента із найвищим середнім балом з певного предмета
    student_highest_avg_grade = session.query(Student.name, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade).join(Subject).filter(Subject.name == subject_name) \
        .group_by(Student.name).order_by(func.avg(Grade.grade).desc()).first()
    
    if student_highest_avg_grade:
        student_name, avg_grade = student_highest_avg_grade
        return student_name, avg_grade
    else:
        return None

def select_3(subject_name):
    # Знайти середній бал у групах з певного предмета
    groups_avg_grade = session.query(Group.name, func.avg(Grade.grade).label('average_grade')) \
        .join(Student, Group.students).join(Grade).join(Subject) \
        .filter(Subject.name == subject_name) \
        .group_by(Group.name).all()
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

def select_11(student_name, teacher_name):
    # Середній бал, який певний викладач ставить певному студентові
    teacher_student_avg_grade = session.query(func.avg(Grade.grade)) \
        .join(Subject).join(Teacher).join(Student) \
        .filter(Student.name == student_name, Teacher.name == teacher_name).scalar()
    return teacher_student_avg_grade

def select_12(group_name, subject_name):
    # Оцінки студентів у певній групі з певного предмета на останньому занятті
    group_subject_last_grades = session.query(Student.name, Grade.grade) \
        .join(Group).join(Grade).join(Subject) \
        .filter(Group.name == group_name, Subject.name == subject_name) \
        .order_by(Grade.date.desc()).first()
    return group_subject_last_grades

# Отримання випадкового предмету
def get_random_subject():
    subjects = session.query(Subject.name).distinct().all()
    return random.choice(subjects)[0]

# Отримання випадкового викладача
def get_random_teacher():
    teachers = session.query(Teacher.name).distinct().all()
    return random.choice(teachers)[0]

# Отримання випадкової групи
def get_random_group():
    groups = session.query(Group.name).distinct().all()
    return random.choice(groups)[0]

# Отримання випадкового студента
def get_random_student():
    students = session.query(Student.name).distinct().all()
    return random.choice(students)[0]

if __name__ == '__main__':
    # Кількість записів для кожного запиту
    num_records = 5

    # Запит 1
    print("\nЗапит 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів:\n")
    result_1 = select_1()
    if result_1:
        for student, avg_grade in result_1:
            print(f"Студент: {student.name}, Середній бал: {avg_grade}")
    else:
        print("Немає результатів")

    # Запити 2-3
    for i in range(2, 4):
        subject_name = get_random_subject()
        print(f"\nЗапит {i}: Результати для предмету '{subject_name}':\n")
        result = globals()[f'select_{i}'](subject_name)
        print(result)

    # Запит 4
    print("\nЗапит 4: Середній бал на потоці:")
    result_4 = select_4()
    print(result_4)

    # Запит 5
    teacher_name = get_random_teacher()
    print(f"\nЗапит 5: Курси, які читає '{teacher_name}':\n")
    result_5 = select_5(teacher_name)
    print(result_5)

    # Запит 6
    group_name = get_random_group()
    print(f"\nЗапит 6: Список студентів '{group_name}'групі:\n")
    result_6 = select_6(group_name)
    print(result_6)

    # Запит 7
    group_name = get_random_group()
    subject_name = get_random_subject()
    print(f"\nЗапит 7: Оцінки студентів у групі '{group_name}' з предмету '{subject_name}':")
    result_7 = select_7(group_name, subject_name)
    print(result_7)

    # Запит 8
    teacher_name = get_random_teacher()
    print(f"\nЗапит 8: Середній бал, який ставить викладач '{teacher_name}':\n")
    result_8 = select_8(teacher_name)
    print(result_8)

    # Запит 9
    student_name = get_random_student()
    print(f"\nЗапит 9: Список курсів, які відвідує студент '{student_name}':\n")
    result_9 = select_9(student_name)
    print(result_9)

    # Запит 10
    student_name = get_random_student()
    teacher_name = get_random_teacher()
    print(f"\nЗапит 10: Список курсів, які читає викладач '{teacher_name}', та відвідує студент '{student_name}':\n")
    result_10 = select_10(student_name, teacher_name)
    print(result_10)

    # Запит 11
    student_name = get_random_student()
    teacher_name = get_random_teacher()
    print(f"\nЗапит 11: Середній бал, який викладач '{teacher_name}' ставить студентові '{student_name}':")
    result_11 = select_11(student_name, teacher_name)
    print(result_11)

    # Запит 12
    group_name = get_random_group()
    subject_name = get_random_subject()
    print(f"\nЗапит 12: Оцінка студента у групі '{group_name}' з предмету '{subject_name}' на останньому занятті:")
    result_12 = select_12(group_name, subject_name)
    print(result_12)