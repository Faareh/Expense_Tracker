from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# Store development data in a local SQLite file
DATABASE_URL = "sqlite:///./expenses.db"

# Manages connections between SQLAlchemy and the database.
engine = create_engine(
    DATABASE_URL,
    # SQLite needs this setting when a FastAPI request uses another thread.
    connect_args={"check_same_thread": False},
)

# Create a new database session for each incoming API request.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    # All SQLAlchemy database models inherit from this base class.
    pass


def get_db():
    # FastAPI injects this session into endpoints through Depends(get_db).
    db = SessionLocal()

    try:
        yield db
    finally:
        # Always return the connection after the request has finished.
        db.close()
