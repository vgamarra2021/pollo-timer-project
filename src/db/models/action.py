from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.models.base import Base

class Action(Base):
    __tablename__ = "action"
    action_id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    type: Mapped[Optional[str]] = mapped_column(String)
    session_id: Mapped[int] = mapped_column(ForeignKey("session.session_id"))
    session: Mapped["Session"] = relationship(back_populates="actions")
