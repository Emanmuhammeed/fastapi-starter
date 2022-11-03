
"""
** Assignment of Routing **
Create a new route within the routers directory called users.py
Enhance users.py to be able to return all users within the application
Enhance users.py to be able to get a single user by a path parameter
Enhance users.py to be able to get a single user by a query parameter
Enhance users.py to be able to modify their current user's password, if passed by authentication
Enhance users.py to be able to delete their own user.
"""

import sys
sys.path.append("..")

from fastapi import Depends, APIRouter
import models
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pydantic import BaseModel
from .auth import  get_current_user ,get_user_exception ,get_password_hash ,verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"users": "not founder"}}
)

models.Base.metadata.create_all(bind=engine)

class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

#Enhance users.py to be able to return all users within the application
@router.get("/user")
async def read_all(db: Session =Depends(get_db)):
    return db.query(models.Todos).all()

#Enhance users.py to be able to get a single user by a path parameter
@router.get("/user/{user_id}")
async def user_by_path(user_id: int, db: Session =Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is not None :
        return user_model
    return " invalid user_id "

#Enhance users.py to be able to get a single user by a query parameter
@router.get("/user/")
async def user_by_query(user_id: int, db: Session =Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is not None :
        return user_model
    return "invalid user_id"

#Enhance users.py to be able to modify their current user's password, if passed by authentication
@router.put("user/password/")
async def user_password_change(user_verification: UserVerification,
                               user: dict=Depends(get_current_user),
                               db: Session =Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if user_model is not None :
        if user_verification == user_model.username and verify_password(
                user_verification.password,
                user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "successful"
    return "invalid user or request"

#Enhance users.py to be able to delete their own user.
router.delete("/user")
async def delete_user(user: dict =Depends(get_current_user), db: Session =Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user_model is None :
        return "invalid user or request"
    db.query(models.Users).filter(models.Users.id == user_id).delete()
    db.commit()
    return "successful Deleted"

