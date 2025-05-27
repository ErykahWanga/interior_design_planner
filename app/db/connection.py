#this file containes the database connection and session management code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalcemy.ext.declarative import declertive_base

Base = declarative_base()
engine = create_engine("sqlite:///../interior_design.db")
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
    
def get_session():
    return Session()

