from sqlalchemy import Column, Integer, String, DateTime
from database import Base  # absolute import from database.py

class House(Base):
    __tablename__ = "house"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    latitude = Column(String, nullable=False)
    longitude = Column(String, nullable=False)
    total_rooms = Column(String, nullable=False)
    population = Column(String, nullable=False)
    households = Column(String, nullable=False)
    median_income = Column(String, nullable=False)
    median_house_value = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
