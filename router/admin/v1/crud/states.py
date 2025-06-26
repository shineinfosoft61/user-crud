from sqlalchemy.orm import Session
from fastapi import HTTPException

from models import StateModel
from libs.utils import now
from router.admin.v1.schemas import StateAdd
from router.admin.v1.crud.countries import get_country_by_id



def get_state_by_id(db: Session, state_id):
    state = db.query(StateModel).filter(StateModel.id == state_id, StateModel.is_deleted == False).first()
    return state


def get_states(
    db: Session,
    start: int,
    limit: int,
    search: str,
    sort_by: str,
    order: str
):
    query = db.query(StateModel).filter(StateModel.is_deleted == False)
    if search:
        query = query.filter(
            StateModel.name.ilike(f"%{search}%")
        )

    if sort_by == "created_at":
        query = query.order_by(StateModel.created_at.desc() if order == "desc" else StateModel.created_at.asc())
    elif sort_by == "name":
        query = query.order_by(StateModel.name.desc() if order == "desc" else StateModel.name.asc())

    total = query.count()
    results = query.offset(start).limit(limit).all()

    return {"data": results, "count": total}


def create_state(db: Session, state: StateAdd):
    country_id = get_country_by_id(db, state.country_id)
    if not country_id:
        raise HTTPException(status_code=404, detail="Country Not Found")
    
    db_state = StateModel(**state.dict())
    db.add(db_state)
    db.commit()
    db.refresh(db_state)
    return db_state


def get_state(db: Session, state_id: int):
    state_obj = get_state_by_id(db, state_id)
    if not state_obj:
        raise HTTPException(status_code= 404, detail= "State Not Found")
    return state_obj


def get_all_states(db: Session):
    return db.query(StateModel).filter(StateModel.is_deleted == False).all()

def update_state(db: Session, state_id: int, state: StateAdd):
    db_state = get_state_by_id(db, state_id)
    if not db_state:
        raise HTTPException(status_code= 404, detail= "State Not Found")
    
    country_id = get_country_by_id(db, state.country_id)
    if not country_id:
        raise HTTPException(status_code=404, detail="Country Not Found")
    
    db_state.name = state.name
    db_state.country_id = state.country_id
    db_state.updated_at = now()
    db.commit()
    db.refresh(db_state)
    return db_state


def delete_state(db: Session, state_id: int):
    db_state = db.query(StateModel).filter(StateModel.id == state_id, StateModel.is_deleted == False).first()
    if db_state:
        db_state.is_deleted = True
        db_state.updated_at = now()
        db.commit()
    return