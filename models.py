from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean

from database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255),index=True)
    dob = Column(Date)
    password = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    otp = Column(String(10))
                          
