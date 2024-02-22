from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Таблиця студентів
class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


# Таблиця груп
class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship("Student", back_populates="group")


# Таблиця викладачів
class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    name = Column(String)


# Таблиця предметів з вказівкою викладача
class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship("Teacher")
    grades = relationship("Grade", back_populates="subject")


# Таблиця оцінок
class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    grade = Column(Integer)
    date = Column(Date)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")


# З'єднання з базою даних
engine = create_engine('postgresql://postgres:My5aK8_U91veR5ty@localhost:5432/fake_universaty')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()