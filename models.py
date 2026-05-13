from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Catalogue(Base):
    __tablename__ = "catalogue"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String)
    releaseYear = Column(Integer)
    description = Column(Text)

from pydantic import BaseModel
from typing import Optional

class CatalogueCreate(BaseModel):
    title: str
    author: str
    publisher: Optional[str] = None
    releaseYear: Optional[int] = None
    description: Optional[str] = None


# SQLite engine
engine = create_engine("sqlite:///libraryRecords.db")

Base.metadata.create_all(engine)