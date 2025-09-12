from sqlalchemy import Boolean,Column ,Integer,String, ForeignKey, Date,Enum,BigInteger 
from sqlalchemy.orm import relationship 
from sqlalchemy.ext.declarative import declarative_base
from .database import Base
import enum
 
class AttendanceStatusEnum(enum.Enum):
    Present = "Present"
    Absent = "Absent"

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    roll_no = Column(String,unique=True,nullable=False)  
    name=Column(String(100),nullable=False)
    batch=Column(String(30),nullable=False)
    gender=Column(String(10),nullable=False)   

    attendance_records = relationship("Attendance",back_populates="student",cascade = "all,delete-orphan") 


class Faculty(Base):
    __tablename__='faculty' 
    faculty_id = Column(String(20),primary_key=True,index=True)    
    name = Column(String(100),nullable=False) 
    phone_no = Column(BigInteger)
    department = Column(String(20))

    subjects = relationship("Subject", back_populates="faculty")



class Subject(Base):
    __tablename__ = 'subjects'
    subj_id = Column(Integer,primary_key = True,autoincrement=True)
    subject_name = Column(String(50),nullable=False) 
    faculty_id = Column(String(20),ForeignKey('faculty.faculty_id')) 

    faculty = relationship("Faculty", back_populates="subjects")
    attendance_records = relationship("Attendance", back_populates="subject")


class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(String, ForeignKey("students.roll_no"))
    subject_id = Column(String, ForeignKey("subjects.subj_id"))
    date = Column(Date)
    status = Column(Enum(AttendanceStatusEnum)) 

    student = relationship("Student", back_populates="attendance_records")
    subject = relationship("Subject", back_populates="attendance_records")   



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum("admin", "faculty", name="user_roles"), default="faculty")





     









