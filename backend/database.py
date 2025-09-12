
from dotenv import load_dotenv
import os
load_dotenv()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



db_url =os.getenv("DB_URL") 


engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()    


 


 

 

