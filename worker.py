from celery import Celery
from app import database, models
from app.sender import email, sms, in_app
from sqlalchemy.orm import Session

celery_app = Celery("worker", broker="pyamqp://guest@localhost//")

@celery_app.task(bind=True, max_retries=3)
def send_notification_task(self, notification_id: int):
    db: Session = next(database.get_db())
    notification = db.query(models.Notification).get(notification_id)

    try:
        if notification.type == "email":
            email.send(notification)
        elif notification.type == "sms":
            sms.send(notification)
        elif notification.type == "in_app":
            in_app.send(notification)

        notification.status = "sent"
    except Exception as e:
        notification.status = "failed"
        db.commit()
        raise self.retry(exc=e, countdown=2 ** self.request.retries)

    db.commit()
