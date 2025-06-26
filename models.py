from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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
    opt_updated_at = Column(DateTime,default=datetime.now)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)

    cities = relationship("CityModel", back_populates="users")

class CountryModel(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

    states = relationship("StateModel", back_populates="country")


class StateModel(Base):
    __tablename__ = 'states'

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

    country = relationship("CountryModel", back_populates="states")
    cities = relationship("CityModel", back_populates="state")


class CityModel(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_deleted = Column(Boolean, default=False)

    state = relationship("StateModel", back_populates="cities")
    users = relationship("UserModel", back_populates="cities")