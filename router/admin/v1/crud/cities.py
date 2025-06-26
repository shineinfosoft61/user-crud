from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import CityModel
from libs.utils import now
from router.admin.v1.schemas import CityAdd
from router.admin.v1.crud.states import get_state_by_id



def get_city_by_id(db: Session, city_id):
    city = db.query(CityModel).filter(CityModel.id == city_id, CityModel.is_deleted == False).first()
    return city


def get_cities(
    db: Session,
    start: int,
    limit: int,
    search: str,
    sort_by: str,
    order: str
):
    query = db.query(CityModel).filter(CityModel.is_deleted == False)
    if search:
        query = query.filter(
            CityModel.name.ilike(f"%{search}%")
        )

    if sort_by == "created_at":
        query = query.order_by(CityModel.created_at.desc() if order == "desc" else CityModel.created_at.asc())
    elif sort_by == "name":
        query = query.order_by(CityModel.name.desc() if order == "desc" else CityModel.name.asc())

    total = query.count()
    results = query.offset(start).limit(limit).all()

    return {"data": results, "count": total}


def create_city(db: Session, city: CityAdd):
    state_id = get_state_by_id(db, city.state_id)
    if not state_id:
        raise HTTPException(status_code=404, detail="State Not Found")
    
    db_city = CityModel(**city.dict())
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_all_cities(db: Session):
    return db.query(CityModel).filter(CityModel.is_deleted == False).all()


def get_city(db: Session, city_id: int):
    db_city = get_city_by_id(db, city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City Not Found")
    return db_city


def update_city(db: Session, city_id: int, city_data: CityAdd):
    db_city = get_city_by_id(db,city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City Not Found")
    
    state_id = get_state_by_id(db, city_data.state_id)
    if not state_id:
        raise HTTPException(status_code=404, detail="State Not Found")
    
    db_city.name = city_data.name
    db_city.state_id = city_data.state_id
    db_city.updated_at = now()
    db.commit()
    db.refresh(db_city)
    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city_by_id(db,city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City Not Found")
    
    db_city.is_deleted = True
    db.commit()
    return db_city
