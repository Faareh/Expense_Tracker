from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db


# Create database tables 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Expense Tracker API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post(
    "/expenses",
    response_model=schemas.ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
):
    # Convert the validated API request into a SQLAlchemy database object
    db_expense = models.Expense(**expense.model_dump())

    # Save the expense and reload it to retrieve generated fields such as its ID
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
