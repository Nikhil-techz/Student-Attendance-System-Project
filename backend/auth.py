from fastapi import APIRouter,Depends,HTTPException,Body
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
from .schemas import  LoginRequest
import bcrypt 

router = APIRouter() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



##Hash password before saving into db

def hash_password(password:str)->str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'),salt) 
    return hashed.decode('utf-8')
def verify_password(password:str,hashed:str)->bool:
    return bcrypt.checkpw(password.encode('utf-8'),hashed.encode('utf-8')) 





@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful", "role": user.role}  