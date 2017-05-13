from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, create_engine, func
from sqlalchemy.orm import Session

engine = create_engine("postgresql://shreyansh@localhost/locations")

Base = declarative_base()

class Location(Base):
    __tablename__ = "locationsTable"
    name = Column(String(50), primary_key = True)
    lat = Column(Float, nullable = False)
    lng = Column(Float, nullable = False)

    def __init__(self, name, lat, lng):
        self.name = name[:50]
        self.lat = lat
        self.lng = lng

##### Alembic is used for database metadata management
##### only execute to reset database
#Base.metadata.drop_all(engine)
#Base.metadata.create_all(engine)
#####

session = Session(engine)
