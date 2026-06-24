from sqlalchemy.orm import Session

from app.repositories.audit_log_repository import (
    create_audit_log,
    get_audit_logs
)


def log_action(
    db: Session,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int,
    details: str | None = None
):
    return create_audit_log(
        db=db,
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )


def get_audit_logs_service(db: Session):
    return get_audit_logs(db=db)