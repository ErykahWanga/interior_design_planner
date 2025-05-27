from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    furniture = relationship('Furniture', back_populates='room', cascade='all, delete-orphan')

    def __init__(self, name, length, width):
        self.name = name
        self.length = float(length)
        self.width = float(width)

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    def total_cost(self, session):
        total = sum(f.cost for f in self.furniture)
        return total or 0.0

    @classmethod
    def all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).get(id)