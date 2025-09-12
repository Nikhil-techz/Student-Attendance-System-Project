from datetime import date
from backend.models import Student, Faculty, Subject, Attendance 
from backend.database import SessionLocal

def get_total_student():
    session  = SessionLocal()
    try:
        return session.query(Student).count()
    finally:
        session.close()

def get_total_faculty():
    session = SessionLocal()
    try:
        return session.query(Faculty).count()
    finally:
        session.close()

def get_total_subject():
    session = SessionLocal()
    try:
        return session.query(Subject).count()
    finally:
        session.close()

def get_present_today():
    session = SessionLocal()
    try:
        return session.query(Attendance).filter(Attendance.date==date.today(), Attendance.status=="Present").count()

    finally:
        session.close()



