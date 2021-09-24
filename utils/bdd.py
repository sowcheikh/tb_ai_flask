from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOSTNAME = '127.0.0.1'
PORT = '5432'
DATABASE = 'postgres'
USERNAME = 'root'
PASSWORD = 'root'

engine = create_engine("postgresql+psycopg2://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE))
Sessionalchemy = sessionmaker(bind=engine)
Base = declarative_base()
