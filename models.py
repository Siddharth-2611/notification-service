from sqlalchemy import Column, Integer, String, Enum, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    type = Column(Enum('email', 'sms', 'in_app', name='notification_types'))
    subject = Column(String, nullable=True)
    message = Column(Text)
    status = Column(Enum('pending', 'sent', 'failed', name='status_types'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
