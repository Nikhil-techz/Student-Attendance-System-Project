from fastapi import FastAPI ,Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal,engine 
from .import models, database,schemas,crud 
from .models import Student, Faculty, Subject, Attendance,User 
from backend.auth import router as auth_router 

app = FastAPI()
app.include_router(auth_router,prefix="/auth") 

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()




## routing of student ## 

@app.post("/students/",response_model=schemas.StudentOut) 
def create_student(student:schemas.StudentCreate,db:Session = Depends(get_db)):
    db_student = crud.get_student_obj_by_roll(db,roll_no=student.roll_no)
    if db_student:
        raise HTTPException(status_code=400,detail="This Roll Number already Exists")
    return crud.create_student(db,student) 





@app.get("/students/", response_model=list[schemas.StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return db.query(models.Student).all() 


@app.get("/students/{roll_no}",response_model=schemas.StudentOut)
def read_student(roll_no:str,db:Session=Depends(get_db)): 
    
    student = db.query(models.Student).filter(models.Student.roll_no == roll_no).first()

    if not student:
        raise HTTPException(status_code=404,detail="student not found")
    return student 




@app.delete("/students/{roll_no}")
def delete_student(roll_no: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_no == roll_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        db.delete(student)
        db.commit()
        return {"message": "Student deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting student: {str(e)}")


#-- routing for faculty-- 


@app.post("/faculties/",response_model=schemas.FacultyOut)
def create_faculty(faculty:schemas.FacultyCreate,db:Session=Depends(get_db)):
    return crud.create_faculty(db,faculty)

@app.get("/faculties/{faculty_id}",response_model=schemas.FacultyOut)
def read_faculty(faculty_id:str,db:Session=Depends(get_db)):
    faculty = crud.get_faculty_by_id(db,faculty_id)

    if not faculty:
        raise HTTPException(status_code=404,detail="faculty not found")
    return faculty
    
##---subject routing---- 




@app.post("/subjects/",response_model=schemas.SubjectsOut)
def create_subject(subject:schemas.SubjectsCreate,db:Session=Depends(get_db)):
    return crud.create_subject(db,subject)

@app.get("/subjects/",response_model=list[schemas.SubjectsOut])
def get_all_subjects(db: Session = Depends(get_db)):
    return db.query(models.Subject).all()  

@app.get("/subjects/{subj_id}",response_model=schemas.SubjectsOut)
def read_subject(subj_id:str,db:Session=Depends(get_db)):
    subject = crud.get_subject_by_id(db,subj_id)   
    if not subject:
        raise HTTPException(status_code=404,detail="subject not found")
    return subject
    

##--attendance routing --- 


@app.post("/attendance/",response_model=schemas.AttendanceOut)
def create_attendance(attendance:schemas.AttendanceCreate,db:Session=Depends(get_db)):
    return crud.mark_attendance(db,attendance)  

@app.get("/attendance/search")
def get_attendance(query:str,db:Session=Depends(get_db)):
    
    ##first try to search by roll no
    attendance_record = crud.get_attendance_by_student_roll(db,query) 
    
    ##otherwise try to search by name
    
    if not  attendance_record:
        attendance_record = crud.get_student_by_name(db,query)

    if not attendance_record:
        raise HTTPException(status_code = 404,detail = "Records not found")
    return attendance_record 


@app.put("/attendance/{roll_no}",response_model = schemas.AttendanceOut)
def update_attendance(roll_no: str, attendance: schemas.AttendanceUpdate, db: Session = Depends(get_db)):
    if attendance.roll_no is None:
        raise HTTPException(status_code=400, detail="Roll number is required")
    return crud.update_attendance_by_roll(db, roll_no, attendance.subject_id, attendance.date, attendance)





@app.get("/")
def read_root():
    return {"message": "Server is running!"} 



                   





