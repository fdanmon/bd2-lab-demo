from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqlconnector://root:bd2_labs_pass@127.0.0.1:3306/bd2_labs")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()