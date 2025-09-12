from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from enum import Enum

class StudentBase(BaseModel):
    name:str
    roll_no:str
    batch : str
    gender:str

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str]
    roll_no:Optional[str]
    batch:Optional[str]
    gender:Optional[str] 


##this class is  used to shows the output - to user. 
class StudentOut(StudentBase):
    id:int

    class Config:
        from_attributes = True 



class FacultyBase(BaseModel):
    faculty_id:str
    name:str
    phone_no:int
    department:str
     
class FacultyCreate(FacultyBase):
    pass

class FacultyUpdate(BaseModel):
    name:Optional[str]
    department:Optional[str]
    phone_no:Optional[int]



class FacultyOut(FacultyBase):
    faculty_id:str
    class Config:
        from_attributes=True


class SubjectsBase(BaseModel):
    subject_name:str 
    subj_id:str
    faculty_id:str

class SubjectsCreate(SubjectsBase):
    pass

class SubjectsUpdate(BaseModel):
    name:Optional[str]
    faculty_id:Optional[str]





class SubjectsOut(SubjectsBase):
    subj_id:str
    class Config:
        from_attributes=True

class AttendanceStatus(str,Enum):
    Present= 'Present'
    Absent = 'Absent'


class AttendanceBase(BaseModel):
    roll_no :str
    subject_id:str
    date:  date  
    status: AttendanceStatus 

class AttendanceCreate(AttendanceBase):
    pass  


class AttendanceUpdate(BaseModel):
    roll_no:str
    subject_id: Optional[str] 
    date: Optional[date]
    status: Optional[str] 

class AttendanceOut(AttendanceBase):
    roll_no:str
    class Config:
        from_attributes=True 


class LoginRequest(BaseModel):
    username: str
    password: str






