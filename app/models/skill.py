from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Skill(Base):

    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer)
    title = Column(String(100))

    def __repr__(self):
        pass