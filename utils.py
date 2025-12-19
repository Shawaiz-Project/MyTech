from models import db, ActivityLog
from flask_login import current_user

def log_activity(action, entity_type, entity_id=None, details=None):
    if current_user and current_user.is_authenticated:
        log = ActivityLog(
            admin_id=current_user.id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            details=details
        )
        db.session.add(log)
        db.session.commit()
