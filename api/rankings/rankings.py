from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from db.database import get_db
from core.config import settings
from services.radarAPI.ranking import get_rankings
from schemas.jsonResponse import jsonResponse


router = APIRouter()

@router.get("/update-rankings/", response_model=jsonResponse)
def update_rankings(language: str):
    language = "en"
    try:
        # fetch rankings data
        rankings_data = get_rankings(language)
        # save in a jsonResponse -- message is necessary, model_dump turns the data into dictionary
        response = jsonResponse(
            message= "Rankings successfully updated",
            data= rankings_data.model_dump()
        )
        
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# def insert_rankings(rankings: jsonResponse, db: Session = Depends(get_db)):
    