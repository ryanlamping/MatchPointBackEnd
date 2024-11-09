from pydantic import BaseModel
from datetime import date

class PlayerSchema(BaseModel):
    id: str
    name: str
    weight: int
    height: int
    nationality: str
    birthdate: date
    hand: int
    biography: str
    coachid: int
    prizemoneywon: float
    gender: int
    professionalrecord: str
    mastersrecord: str
    
    # convert birthday to date
    class Config:
        from_attributes = True  # tells Pydantic to treat SQLAlchemy models as dicts
        @staticmethod
        def serialize_birthday(birthdate: date) -> str:
            return birthdate.isoformat()

        json_encoders = {
            date: serialize_birthday
        }
    