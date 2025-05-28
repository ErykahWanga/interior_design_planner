from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    furniture = relationship('Furniture', back_populates='category')

    def __init__(self, name):
        self.name = name

    def save(self, session):
        session.add(self)
        session.commit()

    @classmethod
    def all(cls, session):
        return session.query(cls).all()