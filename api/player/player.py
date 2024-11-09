from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from db.database import get_db
from core.config import settings
from services.radarAPI.ranking import get_rankings
from schemas.jsonResponse import jsonResponse
from api.rankings.rankings import update_rankings
from services.radarAPI.player import get_player_data

router = APIRouter()

# function to find top 25 players for testing purposes
@router.get("/player_ids/")
def get_players():
    # hard coding language for now
    response = update_rankings("en").model_dump()
        
    # storing competitor_ids
    competitor_ids = []
    
    rankings = response['data']['rankings']
    
    for ranking in rankings:
        competitor_rankings = ranking['competitor_rankings']
        for competitor_ranking in competitor_rankings:
            # Check if the rank is <= 25
            if competitor_ranking['rank'] <= 25:
                competitor = competitor_ranking['competitor']
                competitor_id = competitor['id']
                
                # Append the competitor_id to the list
                competitor_ids.append(competitor_id)
    
    return competitor_ids
    
# rankings data
@router.get("/update-player-info/", response_model=jsonResponse)
def update_player_info(language: str):
    try:
        # fetch rankings data
        rankings_data = get_rankings(language)
        # save in a jsonResponse -- message is necessary, model_dump turns the data into dictionary
        response = jsonResponse(
            message = "Rankings successfully updated",
            data = rankings_data.model_dump()
        )
        
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# def insert_rankings(rankings: jsonResponse, db: Session = Depends(get_db)):

# individual player query
@router.get("/player_query/", response_model=jsonResponse)
def player_query(player_id: str, db: Session = Depends(get_db)):
    try:
        player_data = get_player_data(db, player_id)
        
        response = jsonResponse(
            message = "player data successfully retrieved",
            data = player_data.model_dump()
        )
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    