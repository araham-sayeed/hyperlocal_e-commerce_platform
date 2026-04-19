from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FAQ(Base):
    __tablename__ = "faqs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String(500))
    answer: Mapped[str] = mapped_column(Text)
    region: Mapped[str | None] = mapped_column(String(64), nullable=True)


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_role: Mapped[str] = mapped_column(String(32))
    user_ref: Mapped[str] = mapped_column(String(255))
    issue_description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="open")
    assigned_phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RegionalContact(Base):
    __tablename__ = "regional_contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    area_name: Mapped[str] = mapped_column(String(128))
    support_phone: Mapped[str] = mapped_column(String(32))
