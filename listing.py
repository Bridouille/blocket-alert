from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean

Base = declarative_base()

# This is the model that is going to be saved on the sqlite database
class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key = True)
    blocket_id = Column(String, unique = True)
    link = Column(String, unique = True)
    name = Column(String)
    category = Column(String)
    location = Column(String)
    price = Column(Integer)
    size = Column(Integer)
    rooms = Column(Float)
    date = Column(String)

    def __str__(self):
        return "[{}] => {} SEK/Month {}m2 with {}rooms @{} -- {}".format(self.name, self.price, self.size, self.rooms, self.location, self.date)
