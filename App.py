from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Expense
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Daily Expense Tracker API"}

@app.post("/add-expense/")
def create_expense(title: str, amount: int, db: Session = Depends(get_db)):
    expense = Expense(title=title, amount=amount)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

@app.get("/expenses/{year}/{month}/{day}")
def get_expenses_by_date(year: int, month: int, day: int = None, db: Session = Depends(get_db)):
    try:
        if day:
            filter_date = datetime(year, month, day)
            expenses = db.query(Expense).filter(Expense.date == filter_date).all()
        else:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            expenses = db.query(Expense).filter(Expense.date >= start_date, Expense.date < end_date).all()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")
    
    return expenses

