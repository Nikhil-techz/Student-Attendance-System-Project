import getpass
from sqlalchemy.orm import Session 
from backend.database import SessionLocal
from backend.models import User
from backend.auth import hash_password


def create_user():
    db: Session = SessionLocal()

    username = input("Enter username:")
    password= getpass.getpass("Enter password:")
    role = input("Enter role (default=user):") or "user" 


    if db.query(User).filter(User.username==username).first():
          print(f"user '{username}' already exists")
          db.close()
          return
    
    ## hash password before save
    hashed_pwd = hash_password(password)

    # create a user object
    new_user = User(username=username,password_hash= hashed_pwd,role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    print(f"user created -> username='{username}' ,role= '{role}'")  


if __name__ == "__main__":
     create_user()

     
     

