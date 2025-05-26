from fastapi import APIRouter ,Depends, status, Response, Query
from sqlalchemy.orm import Session
from typing import Optional

from router.admin.v1 import schemas
from dependencies import get_db
from router.admin.v1.crud import user


router = APIRouter()


@router.get("/users", response_model=schemas.UserList)
def list_users(
    start: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at", enum=["created_at", "name", "email"]),
    sort_order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
):
    data = user.get_all_users(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return data



@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user.get_user(db, user_id)
    return db_user


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.User
)
def create_user(users: schemas.Useradd, db: Session = Depends(get_db)):
    db_user = user.create_user(db, users)
    return db_user


@router.put(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["User"]
)
def update_user(
    user_id: int, 
    users: schemas.UserUpdate, 
    db: Session = Depends(get_db)
):
    db_user = user.update_user(db, user_id, users)
    return db_user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/login", 
    response_model=schemas.Token
)
def login_user(payload: schemas.Login, db: Session = Depends(get_db)):
    db_user = user.sign_in(db, payload)
    return db_user



@router.post(
    "/forget-password"
)
def user_forget_password(data: schemas.ForgetPasswordSchema, db: Session = Depends(get_db)):
    db_user = user.forget_password(db,data)
    return db_user


@router.post(
    "/confirm-forget-password"
)
def confirm_forget_password(data: schemas.ConfirmPasswordSchema, db: Session = Depends(get_db)):
    db_user = user.confirm_forget_password(db,data)
    return db_user


@router.post(
    "/change-password"
)
def user_change_password(data: schemas.ChangePasswordSchema, db: Session = Depends(get_db)):
    db_user = user.change_password(db,data)
    return db_user