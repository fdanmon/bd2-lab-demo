from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):

    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    document_number = Column(String(20), nullable=False)
    sex = Column(String(15), nullable=False)
    birth_date = Column(Date, nullable=False)
    phone = Column(String(50), nullable=False)
    rating = Column(Float, nullable=False)

    def __repr__(self):
        return "id: {}\nname: {}\ndocument_number: {}\nsex: {}\nbirth_date: {}\nphone: {}\nrating: {}".format(self.id, self.name, self.document_number, self.sex, self.birth_date, self.phone, self.rating)
        

