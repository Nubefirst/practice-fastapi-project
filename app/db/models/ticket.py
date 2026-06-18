from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.db.database import Base
from app.db.models.enums import TicketStatus


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    status = Column(
        Enum(TicketStatus),
        default=TicketStatus.NEW,
        nullable=False
    )

    creator_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    executor_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    creator = relationship(
        "User",
        foreign_keys=[creator_id],
        back_populates="created_tickets"
    )

    executor = relationship(
        "User",
        foreign_keys=[executor_id],
        back_populates="assigned_tickets"
    )