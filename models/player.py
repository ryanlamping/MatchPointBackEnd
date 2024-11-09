from sqlalchemy import Column, Date, Integer, String
from db.database import Base


# player metadata
class PlayerModel(Base):
    __tablename__ = "player"
    playerid = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(100))
    name = Column(String(100))
    weight = Column(Integer)
    height = Column(Integer)
    nationality = Column(String(3))
    birthdate = Column(Date)
    hand = Column(Integer)
    biography = Column(String(255))
    coachid = Column(Integer)
    prizemoneywon = Column(Integer)
    gender = Column(Integer)
    professionalrecord = Column(String(255))
    mastersrecord = Column(String(255))

    
    
