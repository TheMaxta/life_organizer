# calendar_app/database.py
from sqlalchemy import create_engine, Column, Integer, String, Time, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from calendar_app.models.actions import Frequency

Base = declarative_base()

class ActionDB(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    type = Column(String, nullable=False)
    days = Column(String)  # Store as comma-separated string
    frequency = Column(Enum(Frequency))
    date = Column(Date)

# Create engine and session
engine = create_engine('sqlite:///calendar_app.db')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)