from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date
from sqlalchemy.orm import relationship
from database.db_connector import Base


class DatasetModel(Base):
    __tablename__ = "datasets"

    did = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    author = Column(String, ForeignKey("users.username"), nullable=False)
    description = Column(String(300), nullable=True)
    parent_did = Column(Integer, ForeignKey("datasets.did"), nullable=True)
    create_date = Column(Date, nullable=False)
    last_update = Column(Date, nullable=False)
    user = relationship("UserModel", foreign_keys=[author])
    parent_dataset = relationship("DatasetModel", remote_side=[did])
