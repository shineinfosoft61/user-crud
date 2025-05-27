import bcrypt
import os,traceback,json

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jwcrypto import jwk, jwt
from datetime import datetime, timedelta
from jwcrypto.jwt import JWTExpired


from models import UserModel
from libs.utils import hash_password, now, get_user_by_id, get_user_by_email, object_as_dict,generate_otp,send_email
from router.admin.v1.schemas import Useradd,UserUpdate,Login,ForgetPassword,ConfirmPassword,ChangePassword,User
from libs.utils import verify_password, hash_password
load_dotenv()



def get_all_users(
    db: Session,
    start: int,
    limit: int,
    search: str,
    sort_by: str,
    sort_order: str
):
    query = db.query(UserModel).filter(UserModel.is_deleted == False)
    if search:
        query = query.filter(
            UserModel.name.ilike(f"%{search}%") |
            UserModel.email.ilike(f"%{search}%")
        )

    if sort_by == "created_at":
        query = query.order_by(UserModel.created_at.desc() if sort_order == "desc" else UserModel.created_at.asc())
    elif sort_by == "name":
        query = query.order_by(UserModel.name.desc() if sort_order == "desc" else UserModel.name.asc())
    elif sort_by == "email":
        query = query.order_by(UserModel.email.desc() if sort_order == "desc" else UserModel.email.asc())

    total = query.count()
    results = query.offset(start).limit(limit).all()

    return {"data": results, "count": total}


def get_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(db: Session, user: Useradd):
    existing_user = get_user_by_email(db,user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="User already exists")

    db_user = UserModel(
        name=user.name,
        email=user.email,
        dob=user.dob,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user.name
    db_user.dob = user.dob
    db_user.updated_at = now()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_deleted = True
    db_user.updated_at = now()
    db.commit()


def get_token(user_id: int, email: str):
    raw_key = os.getenv("JWT_KEY")
    if not raw_key:
        raise ValueError("JWT_KEY is missing from environment variables")

    try:
        key_dict = json.loads(raw_key)
        key = jwk.JWK(**key_dict)
    except json.JSONDecodeError:
        raise ValueError("Invalid JWT_KEY format. It must be a valid JSON string.")

    payload = {
        "id": user_id,
        "email": email,
        "exp": int((datetime.now() + timedelta(hours=1)).timestamp())
    }

    token = jwt.JWT(header={"alg": "HS256"}, claims=payload)
    token.make_signed_token(key)
    return token.serialize()


def verify_token(db: Session, token: str):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        key = json.loads(os.getenv("JWT_KEY"))
        jwk_key = jwk.JWK(**key)

        decoded_token = jwt.JWT(key=jwk_key, jwt=token)
        claims = json.loads(decoded_token.claims)

        db_user = get_user_by_id(db, user_id=claims["id"])
        if db_user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return db_user

    except JWTExpired as e:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception as e:
        print("Error:", e)
        print(traceback.format_exc())
        raise HTTPException(status_code=401, detail="Invalid token")


def sign_in(db: Session, data: Login):
    db_user = get_user_by_email(db, data.email)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    hashed = db_user.password
    hashed = bytes(hashed, "utf-8")
    password = bytes(data.password, "utf-8")
    if not bcrypt.checkpw(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_data = User.from_orm(db_user).dict()
    user_data["access_token"] = get_token(db_user.id, db_user.email)
    return user_data



def forget_password(db: Session, data: ForgetPassword):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = generate_otp()
    user.otp = otp
    user.opt_updated_at = now()
    db.commit()

    send_email(
        recipient=user.email,
        subject="Your OTP Code",
        content=f"Your OTP is {otp}"
    )
    return {"message": "OTP sent to your email"}


def confirm_forget_password(db: Session, data: ConfirmPassword):
    user = get_user_by_email(db, data.email)

    if not user or user.otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid email or OTP")

    if  datetime.now() > user.opt_updated_at + timedelta(minutes=10):
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    user.password = hash_password(data.password)
    user.otp = None
    db.commit()
    return {"message": "Password reset successful"}


def change_password(db: Session, data: ChangePassword, user_obj: str):    
    if not verify_password(data.old_password, user_obj.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user_obj.password = hash_password(data.new_password)
    db.commit()
    db.refresh(user_obj)
    return {"message": "Password update successfull"}
