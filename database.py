from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔁 Replace these credentials with your actual MySQL DB info
DATABASE_URL = "mysql+pymysql://root:Root@localhost/expense_tracker"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
