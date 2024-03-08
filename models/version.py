from sqlalchemy import Column, Integer, String, ForeignKey, Date, ARRAY, JSON, func
from sqlalchemy.orm import relationship
from database.db_connector import Base


class VersionModel(Base):
    __tablename__ = "versions"

    vid = Column(Integer, primary_key=True)
    num = Column(Integer)
    did = Column(Integer, ForeignKey("datasets.did"))
    version_date = Column(Date, server_default=func.now())
    specs = Column(JSON)
    feature_versions = Column(ARRAY(String))
    collaborator = Column(Integer, ForeignKey("users.uid"))
    user = relationship("UserModel", foreign_keys=[collaborator])
    dataset = relationship("DatasetModel", foreign_keys=[did])
