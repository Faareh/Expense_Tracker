from fastapi import Depends, FastAPI, status, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

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

@app.get("/expenses", response_model=list[schemas.ExpenseResponse])
def list_expenses(db: Session = Depends(get_db)):
    # Retrieve every expense, ordered from newest to oldest.
    statement = select(models.Expense).order_by(models.Expense.id.desc())
    return db.scalars(statement).all()


@app.get("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(models.Expense, expense_id)

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    return expense

@app.put("/expenses/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
    expense_id: int,
    updated_expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db),
):
    expense = db.get(models.Expense, expense_id)

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    # Replace the existing values with the validated request values
    for field, value in updated_expense.model_dump().items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense


@app.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.get(models.Expense, expense_id)

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Expense not found",
        )

    db.delete(expense)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)