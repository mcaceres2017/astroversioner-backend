from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db_connector import Base


class VersionObjectModel(Base):
    __tablename__ = "version_objects"

    id = Column(Integer, primary_key=True)
    versions = Column(Integer, ForeignKey("versions.vid"))
    objects = Column(String, ForeignKey("objects.oid"))
    version = relationship("VersionModel", foreign_keys=[versions])
    object = relationship("ObjectModel", foreign_keys=[objects])
