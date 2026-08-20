from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Date, DateTime, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

# Maps to the "expenses" table in SQLite.
class Expense(Base):
    __tablename__ = "expenses"

    # The database automatically generates the primary-key ID.
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200))
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(100))
    expense_date: Mapped[date] = mapped_column(Date)
    # Record creation times in UTC so they remain consistent across deployments.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
