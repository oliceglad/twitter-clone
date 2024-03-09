import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

engine = create_engine(os.getenv("DATABASE"))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
