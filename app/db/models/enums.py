import enum


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class TicketStatus(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"