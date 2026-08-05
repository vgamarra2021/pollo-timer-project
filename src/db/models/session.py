from typing import Optional
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.models.base import Base

class Session(Base):
    __tablename__ = "session"
    session_id: Mapped[int] = mapped_column(primary_key=True)
    seconds_duration: Mapped[Optional[float]] = mapped_column(Numeric)
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean)
    started_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    finish_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
