import os
import smtplib
import random

from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from pydantic import EmailStr
from email.message import EmailMessage
from dotenv import load_dotenv

from models import UserModel

load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def now():
    return datetime.now()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(UserModel).filter(UserModel.id == user_id, UserModel.is_deleted == False).first()
    return user


def get_user_by_email(db: Session, email: EmailStr):
    existing_user = db.query(UserModel).filter(UserModel.email == email,UserModel.is_deleted == False).first()
    return existing_user

def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(recipient, subject, content):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_FROM")
    msg['To'] = recipient
    msg.set_content(content)

    with smtplib.SMTP(os.getenv("EMAIL_SERVER"), int(os.getenv("EMAIL_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_FROM"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)