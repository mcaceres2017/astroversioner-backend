from sqlalchemy import Column, String
from database.db_connector import Base


class ObjectModel(Base):
    __tablename__ = "objects"

    oid = Column(String, primary_key=True)
    _class = Column("class", String)
