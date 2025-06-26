from fastapi import APIRouter ,Depends, status, Response, Query, Header
from sqlalchemy.orm import Session
from typing import Optional
from fastapi_cache.decorator import cache

from router.admin.v1 import schemas
from dependencies import get_db
from router.admin.v1.crud import cities, countries, states, user


router = APIRouter()


@router.get(
    "/users",
    response_model=schemas.UserList,
    tags=["User"]
)
def list_users(
    start: int = 0,
    limit: int = 10,
    city_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at", enum=["created_at", "name", "email"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    data = user.get_all_users(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order,
        city_id=city_id
    )
    return data



@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    tags=["User"]
)
def get_user(
    user_id: int, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    db_user = user.get_user(db, user_id)
    return db_user


@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED, 
    response_model=schemas.User,
    tags=["User"]
)
def create_user(
    users: schemas.Useradd,
    db: Session = Depends(get_db)
):
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
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    db_user = user.update_user(db, user_id, users)
    return db_user


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    tags=["User"]
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    user.delete_user(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/login", 
    response_model=schemas.LoginResponse,
    tags=["User - Auth"]
)
def login_user(
    data: schemas.Login, 
    db: Session = Depends(get_db)
):
    db_user = user.sign_in(db, data)
    return db_user



@router.post(
    "/forget-password",
    tags=["User - Auth"]
)
def user_forget_password(
    data: schemas.ForgetPassword, 
    db: Session = Depends(get_db)
):
    db_user = user.forget_password(db,data)
    return db_user


@router.post(
    "/confirm-forget-password",
    tags=["User - Auth"]
)
def confirm_forget_password(
    data: schemas.ConfirmPassword,
    db: Session = Depends(get_db)
):
    db_user = user.confirm_forget_password(db,data)
    return db_user


@router.post(
    "/change-password",
    tags=["User - Auth"]
)
def user_change_password(
    data: schemas.ChangePassword,
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user_obj = user.verify_token(db, token)
    db_user = user.change_password(db,data,user_obj)
    return db_user


@router.get(
    "/countries/all",
    response_model=list[schemas.Country],
    tags = ["Country"]
)
@cache(expire=60)
async def get_all_countries(
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return await countries.get_all_countries_cached()


@router.post(
    "/countries",
    response_model=schemas.Country,
    tags = ["Country"]
)
def create_country(
    country: schemas.CountryAdd, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    country_obj = countries.create_country(db, country)
    return country_obj


@router.get(
    "/countries/{country_id}", 
    response_model=schemas.Country,
    tags = ["Country"],
)
async def get_country(
    country_id: int, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):  
    user.verify_token(db, token)
    db_country = countries.get_country(db, country_id)
    return await db_country


@router.get(
    "/countries", 
    response_model=schemas.CountryList,
    tags = ["Country"]
)
def get_countries(
    start: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at", enum=["created_at", "name"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return countries.get_countries(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order
    )


@router.put(
    "/countries/{country_id}", 
    response_model=schemas.Country,
    tags = ["Country"]
)
def update_country(
    country_id: int, 
    country: schemas.CountryAdd, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    data = countries.update_country(db, country_id, name=country.name)
    return data


@router.delete(
    "/countries/{country_id}",
    tags = ["Country"]
)
def delete_country(
    country_id: int, db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    countries.delete_country(db, country_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/states",
    response_model=schemas.State,
    tags = ["State"]
)
def create_state(
    state: schemas.StateAdd, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return states.create_state(db, state)


@router.get(
    "/states/all",
    response_model=list[schemas.State],
    tags = ["State"]
)
def get_all_states(
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return states.get_all_states(db)


@router.get(
    "/states/{state_id}",
    response_model=schemas.State,
    tags = ["State"]
)
def get_state(
    state_id: int,
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    db_state = states.get_state(db, state_id)
    return db_state


@router.get(
    "/states", 
    response_model=schemas.StateList,
    tags = ["State"]
)
def get_states(
    start: int = 0,
    limit: int = 10,
    search: str = Query(None),
    sort_by: str = Query("created_at", enum=["created_at", "name"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return states.get_states(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order
    )


@router.put(
    "/states/{state_id}",
    response_model=schemas.State,
    tags = ["State"]
)
def update_state(
    state_id: int,
    state: schemas.StateAdd, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    db_state = states.update_state(db, state_id, state)
    return db_state


@router.delete(
    "/states/{state_id}",
    tags = ["State"]
)
def delete_state(
    state_id: int,
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    states.delete_state(db, state_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/cities",
    response_model=schemas.CityList,
    tags=["City"]
)
def get_cities(
    start: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None),
    sort_by: str = Query("created_at", enun=["created_at", "name"]),
    order: str = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return cities.get_cities(
        db=db,
        start=start,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order
    )


@router.post(
    "/cities",
    response_model=schemas.City,
    tags = ["City"]
)
def create_city(
    city: schemas.CityAdd, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return cities.create_city(db, city)


@router.get(
    "/cities/all", 
    response_model=list[schemas.City],
    tags = ["City"]
)
def get_all_cities(
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    return cities.get_all_cities(db)


@router.get(
    "/cities/{city_id}", 
    response_model=schemas.City,
    tags = ["City"]
)
def get_city(
    city_id: int, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    city = cities.get_city(db, city_id)
    return city


@router.put(
    "/cities/{city_id}", 
    response_model=schemas.City,
    tags = ["City"]
)
def update_city(
    city_id: int, city: schemas.CityAdd, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    updated_city = cities.update_city(db, city_id, city)
    return updated_city


@router.delete(
    "/cities/{city_id}", 
    response_model=schemas.City,
    tags = ["City"]
)
def delete_city(
    city_id: int, 
    db: Session = Depends(get_db),
    token: str = Header(None),
):
    user.verify_token(db, token)
    cities.delete_city(db, city_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)