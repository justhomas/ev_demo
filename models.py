from sqlalchemy import  Column, Integer, String, Float
from database import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    street = Column(String, )
    state = Column(String, )
    latitude = Column(Float)
    longitude = Column(Float)
