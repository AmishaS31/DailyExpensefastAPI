
from sqlalchemy import Column, Integer, String, Float, DateTime, func
from database import Base

class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    # Stores the date/time when the record is created
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
     # Updates the date/time whenever the record is modified
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



   