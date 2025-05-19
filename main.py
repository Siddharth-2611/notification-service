
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.worker import send_notification_task

app = FastAPI()

@app.post("/notifications")
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(database.get_db)):
    db_notification = models.Notification(**notification.dict(), status="pending")
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    # Send to Celery worker
    send_notification_task.delay(db_notification.id)

    return {"message": "Notification queued", "id": db_notification.id}

@app.get("/users/{user_id}/notifications")
def get_notifications(user_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Notification).filter(models.Notification.user_id == user_id).all()
