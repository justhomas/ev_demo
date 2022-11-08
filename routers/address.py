from fastapi import APIRouter, Depends, HTTPException
from typing import List
import schemas
from database import get_db
from sqlalchemy.orm import Session
import models
from sqlalchemy import select, update, delete, values, text
from haversine import haversine #haversine library implements the haversine formula to calculate distance between two points

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    responses={404: {"description": "Address Not found"}},
)


@router.get("/",response_model=List[schemas.Address])
def get_addresses( db: Session = Depends(get_db),latitude: float =0,longitude:float =0, distance:float=0):
    """
    API to get a list of all addresses.

    Use the latitude,longitude and distance fields to filter on data
    """
    
    # This approach is not ideal in terms of performance. 
    # SQLite has limitations on math functions based on how it is compiled.
    # Haversine formula depends on math functions such as acos, cos etc...

    q = db.query(models.Address).all()
    if(latitude or longitude or distance): 
        s =[]
        for address in q:
           if haversine((latitude,longitude), (address.latitude,address.longitude)) <=distance:
            s.append(address)
        q=s
    
    return q

@router.post("/",response_model=schemas.Address)
def create_address(address: schemas.AddressCreate,db: Session = Depends(get_db)):
    """
    API to create a new address
    """
    db_address = models.Address(street=address.street,city=address.city,state=address.state,latitude=address.latitude,longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@router.get("/{address_id}",response_model=schemas.Address)
def get_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@router.delete("/{address_id}",status_code=204)
def delete_address(address_id: int,db: Session = Depends(get_db)) -> None:
    db.execute(delete(models.Address).where(models.Address.id == address_id))
    db.commit()    

@router.patch("/{address_id}",response_model=schemas.Address)
def update_address(address_id: int, address:schemas.AddressCreate, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    upd = update(models.Address).values(address.dict()).where(models.Address.id == address_id)
    db.execute(upd)
    db.commit()
    db.refresh(db_address)
    return db_address
