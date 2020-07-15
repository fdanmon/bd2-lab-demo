from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Job(Base):

    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    vacancies = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False)
    company_id = Column(Integer, nullable=False)
    expiration_date = Column(DateTime, nullable=True)
    status = Column(Integer, nullable=False)

    def __repr__(self):
        pass

    def __init__(self, title, description, vacancies, category_id, company_id, status):
        self.title = title
        self.description = description
        self.vacancies = vacancies
        self.category_id = category_id
        self.company_id = company_id
        self.expiration_date = '2020-12-31'
        self.status = status
