from .db import *
from sqlalchemy import Column, Integer, String, DateTime

class Category(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, name):
        self.title = title
        self.name = name
