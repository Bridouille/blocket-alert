from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from listing import *

# Databse helper to SELECT and INSERT into the databse
class Db:
    def __init__(self, dbName = "listings.db"):
        self.engine = create_engine('sqlite:///' + dbName, echo = False)
        self.session = sessionmaker(bind = self.engine)()
        Base.metadata.create_all(self.engine)

    def isPresent(self, blocket_id = ""):
        return self.session.query(Listing).filter_by(blocket_id = blocket_id).first() is not None

    def add(self, listing):
        self.session.add(listing)
        self.session.commit()
