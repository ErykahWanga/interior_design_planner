from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.connection import Base

class Furniture(Base):
    __tablename__ = 'furniture'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    room = relationship('Room', back_populates='furniture')
    category = relationship('Category', back_populates='furniture')

    def __init__(self, name, cost, room_id, category_id):
        self.name = name
        self.cost = float(cost)
        self.room_id = room_id
        self.category_id = category_id

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()