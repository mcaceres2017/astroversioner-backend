from sqlalchemy import Column, Integer, String
from database.db_connector import Base


class UserModel(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    mail = Column(String(100), unique=True)
    username = Column(String(30), unique=True)
    password = Column(String(30))
