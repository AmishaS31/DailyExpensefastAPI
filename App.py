from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Expense

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

@app.get("/expenses/")
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()
