from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Company(Base):

    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer)
    name = Column(String(200), nullable=False)
    document_number = Column(String(20), nullable=False)
    rating = Column(Float, nullable=False)
    phone = Column(String(30), nullable=False)

    def __repr__(self):
        return "id: {}\nname: {}\ndocument_number: {}\category_id: {}\rating: {}\nphone: {}".format(self.id, self.name, self.document_number, self.category_id, self.rating, self.phone)

