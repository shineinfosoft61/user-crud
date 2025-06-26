from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi_cache.decorator import cache

from dependencies import get_db
from models import CountryModel
from libs.utils import now
from router.admin.v1.schemas import CountryAdd


def get_country_by_id(db: Session, country_id: int):
    country = db.query(CountryModel).filter(CountryModel.id == country_id, CountryModel.is_deleted == False).first()
    return country


def get_countries(
    db: Session,
    start: int,
    limit: int,
    search: str,
    sort_by: str,
    order: str
):
    query = db.query(CountryModel).filter(CountryModel.is_deleted == False)
    if search:
        query = query.filter(
            CountryModel.name.ilike(f"%{search}%")
        )

    if sort_by == "created_at":
        query = query.order_by(CountryModel.created_at.desc() if order == "desc" else CountryModel.created_at.asc())
    elif sort_by == "name":
        query = query.order_by(CountryModel.name.desc() if order == "desc" else CountryModel.name.asc())

    total = query.count()
    results = query.offset(start).limit(limit).all()

    return {"data": results, "count": total}


def create_country(db: Session, country: CountryAdd):
    db_country = CountryModel(**country.dict())
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country


def get_country(db: Session, country_id: int):
    country = get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


# async def get_all_countries_from_db(db: Session):
#     return db.query(CountryModel).filter(CountryModel.is_deleted == False).all()

async def get_all_countries_cached():
    print("Fetching from DB...")
    db = next(get_db())
    try:
        return db.query(CountryModel).filter(CountryModel.is_deleted == False).all()
    finally:
        db.close()

    

def update_country(db: Session, country_id: int, name: str):
    db_country = get_country_by_id(db, country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    db_country.name = name
    db_country.updated_at = now()
    db.commit()
    db.refresh(db_country)
    return db_country


def delete_country(db: Session, country_id: int):
    db_country = get_country_by_id(db, country_id)
    if not db_country:
        raise HTTPException(status_code=404, detail="Country not found")
    db_country.is_deleted = True
    db.commit()
    return db_country