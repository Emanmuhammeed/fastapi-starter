from sqlalchemy import BOOLEAN, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Users(Base):
   __tablename__ = "users"

   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, unique=True, index=True)
   username = Column(String, unique=True, index=True)
   first_name = Column(String)
   last_name = Column(String)
   hash_password = Column(String)
   is_active = Column(BOOLEAN, default=True)

   todos = relationship("Todos", back_populates="owner")


class Todos(Base):
   __tablename__ = "todos"

   id = Column(Integer, primary_key=True, index=False)
   title = Column(String)
   description = Column(String)
   priority = Column(Integer)
   complete = Column(BOOLEAN, default=False)
   owner_id = Column(Integer, ForeignKey("users.id"))

   owner = relationship("Users", back_populates="todos")
