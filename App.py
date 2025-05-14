from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
from models import Expense
from datetime import datetime

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/api-docs")

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

# POST - Create new expense
@app.post("/add-expense/")
def create_expense(name: str, title: str, amount: float, db: Session = Depends(get_db)):
    expense = Expense(name=name, title=title, amount=amount)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

# GET - Get expenses by date
@app.get("/expenses/{year}/{month}/{day}")
def get_expenses_by_date(year: int, month: int, day: int = None, db: Session = Depends(get_db)):
    try:
        if day:
            filter_date = datetime(year, month, day)
            expenses = db.query(Expense).filter(Expense.created_at == filter_date).all()
        else:
            start_date = datetime(year, month, 1)
            if month == 12:
                end_date = datetime(year + 1, 1, 1)
            else:
                end_date = datetime(year, month + 1, 1)
            expenses = db.query(Expense).filter(
                Expense.created_at >= start_date,
                Expense.created_at < end_date
            ).all()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date")
    
    return expenses

# PUT - Update existing expense
@app.put("/update-expense/{expense_id}")
def update_expense(
    expense_id: int = Path(..., description="The ID of the expense to update"),
    name: str = None,
    title: str = None,
    amount: float = None,
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    if name is not None:
        expense.name = name
    if title is not None:
        expense.title = title
    if amount is not None:
        expense.amount = amount

    expense.updated_at = datetime.now()

    db.commit()
    db.refresh(expense)
    return expense

# DELETE - Remove expense by ID
@app.delete("/delete-expense/{expense_id}")
def delete_expense(
    expense_id: int = Path(..., description="The ID of the expense to delete"),
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"message": f"Expense with ID {expense_id} has been deleted successfully."}



# from fastapi import FastAPI, Depends, HTTPException, Path
# from sqlalchemy.orm import Session
# from database import engine, Base, SessionLocal
# from models import Expense
# from datetime import datetime

# # Create tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(docs_url="/api-docs")

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @app.get("/")
# def read_root():
#     return {"message": "Welcome to Daily Expense Tracker API"}

# @app.post("/add-expense/")
# def create_expense(name: str, title: str, amount: float, db: Session = Depends(get_db)):
#     expense = Expense(name=name, title=title, amount=amount)
#     db.add(expense)
#     db.commit()
#     db.refresh(expense)
#     return expense

# @app.get("/expenses/{year}/{month}/{day}")
# def get_expenses_by_date(year: int, month: int, day: int = None, db: Session = Depends(get_db)):
#     try:
#         if day:
#             filter_date = datetime(year, month, day)
#             expenses = db.query(Expense).filter(Expense.created_at == filter_date).all()
#         else:
#             start_date = datetime(year, month, 1)
#             if month == 12:
#                 end_date = datetime(year + 1, 1, 1)
#             else:
#                 end_date = datetime(year, month + 1, 1)
#             expenses = db.query(Expense).filter(Expense.created_at >= start_date, Expense.created_at < end_date).all()
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date")
    
#     return expenses

# @app.put("/update-expense/{expense_id}")
# def update_expense(
#     expense_id: int = Path(..., description="The ID of the expense to update"),
#     name: str = None,
#     title: str = None,
#     amount: float = None,
#     db: Session = Depends(get_db)
# ):
#     expense = db.query(Expense).filter(Expense.id == expense_id).first()

#     if not expense:
#         raise HTTPException(status_code=404, detail="Expense not found")

#     if name is not None:
#         expense.name = name
#     if title is not None:
#         expense.title = title
#     if amount is not None:
#         expense.amount = amount

#     expense.updated_at = datetime.now()

#     db.commit()
#     db.refresh(expense)
#     return expense

