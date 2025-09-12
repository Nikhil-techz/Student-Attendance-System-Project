from fastapi import HTTPException 
import re
from sqlalchemy.orm import Session
from backend import models,schemas
from backend.models import Student,Faculty,Subject,Attendance
from .schemas import StudentCreate, FacultyCreate,SubjectsCreate,AttendanceCreate, StudentUpdate,FacultyUpdate,SubjectsUpdate,AttendanceUpdate
from datetime import date , time

## student-- 

## data validation for student roll - no:
def is_valid_roll(roll_no:str) -> bool:
    pattern = r"^\d{4}[A-Za-z]{3}\d{3}$" 
    return bool(re.match(pattern,roll_no)) 


def create_student(db:Session,student: StudentCreate):
    if not is_valid_roll(student.roll_no):
        raise HTTPException(status_code=400,detail="Invalid Roll Number Format") 
    existing_student = get_student_obj_by_roll(db,student.roll_no)
    if existing_student:
        raise HTTPException(status_code=400,detail="Student with this roll number is already exists")
    db_student = Student(**student.dict())   
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student 

def get_student_by_roll(db:Session,roll_no:str):
    query = (db.query(Attendance.roll_no,
            Student.name.label("name") , 
            Subject.subject_name,
            Faculty.name.label("faculty_name"),
            Attendance.date,
            Attendance.status
        ).join(Student,Attendance.roll_no == Student.roll_no)
         .join(Subject, Attendance.subject_id == Subject.subj_id)
        .join(Faculty, Subject.faculty_id == Faculty.faculty_id)
        .filter(Student.roll_no == roll_no)
        .distinct()
        .all() )
    
    return [
        {
            "roll_no": row.roll_no,
            "name": row.name,
            "subject_name": row.subject_name,
            "faculty_name": row.faculty_name,
            "date": row.date.strftime("%Y-%m-%d") if row.date else None,
            "status": row.status
        }
        for row in query
    ] 
        

def get_student_by_name(db:Session,name:str):

    query = ( 
        db.query(
            Attendance.roll_no,
            Student.name,
            Subject.subject_name,
            Faculty.name.label("faculty_name"),
            Attendance.date,
            Attendance.status
        ) 
        .join(Student, Attendance.roll_no == Student.roll_no)
        .join(Subject, Attendance.subject_id == Subject.subj_id)
        .join(Faculty, Subject.faculty_id == Faculty.faculty_id)
        .filter(Student.name.ilike(f"%{name}%"))  
        .distinct()
        .all()  
    )

    return [
        {
            "roll_no": row.roll_no,
            "name": row.name,
            "subject_name": row.subject_name,
            "faculty_name": row.faculty_name,
            "date": row.date.strftime("%Y-%m-%d") if row.date else None,
            "status": row.status
        }
        for row in query
    ]

def get_student_obj_by_roll(db:Session,roll_no:str):
    """Return the student orm ojeect for(update /delete)"""
    return db.query(Student).filter(Student.roll_no==roll_no).first()


def update_student_by_roll(db: Session, roll_no:str, student_data: StudentUpdate):

    student = get_student_obj_by_roll(db, roll_no) 
    if not student:
        raise HTTPException(status_code=404, detail="Student not found") 
    for field, value in student_data.dict(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()
    db.refresh(student) 
    return student  

def delete_student_by_roll(db: Session, roll_no: str):
    try:
        student = get_student_obj_by_roll(db, roll_no) 
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        db.delete(student)
        db.commit()
        return student

    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))  
 


## faculty### 

##data validation for faculty id. 
def valid_faculty_id(faculty_id:str) -> bool:
    pattern = r"^\d{4}[A-Z]{3,4}\d{3}$" 
    return bool(re.match(pattern,faculty_id))

def create_faculty(db: Session, faculty: FacultyCreate):
    if not valid_faculty_id(faculty.faculty_id):
        raise HTTPException(status_code=404, detail="Invalid faculty ID format")
    
    existing_faculty = get_faculty_by_id(db, faculty.faculty_id)
    if existing_faculty:
        raise HTTPException(status_code=400, detail="Faculty with this ID already exists")
    
    db_faculty = Faculty(**faculty.dict())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty 

def get_faculty_by_id(db:Session,faculty_id:str):
    return db.query(Faculty).filter(Faculty.faculty_id==faculty_id).first() 


def update_faculty(db: Session, faculty_id: str, faculty_data: FacultyUpdate):
    faculty = get_faculty_by_id(db, faculty_id)
    if not faculty:
        return None
    for field, value in faculty_data.dict(exclude_unset=True).items():
        setattr(faculty, field, value)
    db.commit()
    db.refresh(faculty)
    return faculty


def delete_faculty(db:Session,faculty_id:str):
    faculty = get_faculty_by_id(db,faculty_id)
    if not faculty:
        return None
    db.delete(faculty)
    db.commit()
    return faculty


##subject ## 

##data validation for subject id: 
def valid_subject_id(subj_id:str)->bool:
    pattern =  r"^[A-Z]{2,4}\d{3}$" 
    return bool(re.match(pattern,subj_id)) 


def create_subject(db: Session, subject: SubjectsCreate):
    if not valid_subject_id(subject.subj_id):
        raise HTTPException(status_code = 404,detail="Invalid subject id")
    existing_subject_id = get_subject_by_id(db,subject.subj_id)
    if existing_subject_id:
        raise HTTPException(status_code=404,detail= "subject id is already exists") 
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject_by_id(db: Session, subject_id: str):
    return db.query(Subject).filter(Subject.subj_id == subject_id).first()

def update_subject(db: Session, subject_id: int, subject_data: SubjectsUpdate):
    subject = get_subject_by_id(db, subject_id)
    if not subject:
        return None
    for field, value in subject_data.dict(exclude_unset=True).items():
        setattr(subject, field, value)
    db.commit()
    db.refresh(subject)
    return subject

def delete_subject(db: Session, subject_id: str):
    subject = get_subject_by_id(db, subject_id)
    if not subject:
        return None
    db.delete(subject) 
    db.commit()
    return subject



##attendance ## 
def mark_attendance(db: Session, attendance: AttendanceCreate):
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance 

def get_attendance_by_student_roll(db: Session, roll_no: str):
    query = (
        db.query(
            Attendance.roll_no,
            Student.name.label("name"),
            Subject.subject_name,
            Faculty.name.label("faculty_name"),
            Attendance.date,
            Attendance.status
        )
        .join(Student, Attendance.roll_no == Student.roll_no)
        .join(Subject, Attendance.subject_id == Subject.subj_id)
        .join(Faculty, Subject.faculty_id == Faculty.faculty_id)
        .filter(Student.roll_no == roll_no)
        .all()
    )

    return [
        {
            "roll_no": row.roll_no,
            "name": row.name,
            "subject_name": row.subject_name,
            "faculty_name": row.faculty_name,
            "date": row.date.strftime("%Y-%m-%d") if row.date else None,
            "status": row.status
        }
        for row in query
    ]

def update_attendance_by_roll(db: Session, roll_no:str,subject_id:str,date:date, attendance_data: AttendanceUpdate):

    #get the student by roll no:
    student = db.query(Student).filter(Student.roll_no==roll_no).first() 
    if not student:
        raise HTTPException(status_code = 404,detail="student not found")
    #get the attendance record
    attendance = db.query(Attendance).filter(Attendance.student_id == student.id,
            Attendance.subject_id == subject_id,
            Attendance.date == date).first()
    if not attendance:
       raise HTTPException(status_code=404, detail="Attendance record not found")  

    for field, value in attendance_data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(attendance, field, value)  

    db.commit()
    db.refresh(attendance)
    return attendance 



