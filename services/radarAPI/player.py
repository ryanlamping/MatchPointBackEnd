from fastapi import HTTPException
import requests
from core.config import settings
from models.player import PlayerModel
from schemas.player import PlayerSchema
from sqlalchemy.orm import Session


# setting api url for rankings
API_URL = "https://api.sportradar.com/tennis/trial/v3/"

# update with language of ios from frontend
language = "en"

# format
format = "json"

# radar api key
API_KEY = settings.RADAR_API_KEY

# make headers
headers = {"accept": "application/json"}

def calculate_overall_record(data):
    # receives in competitor rankings
    # performance record kpis
    overall_record = {
        "total_competitions_played": 0,
        "total_competitions_won": 0,
        "total_matches_played": 0,
        "total_matches_won": 0
    }
    
    # for each year
    for period in data["periods"]:
        # increase kpi by number in period
        # overall_record["total_competitions_played"] += period["statistics"]["competitions_played"]
        # overall_record["total_competitions_won"] += period["statistics"]["competitions_won"]
        overall_record["total_matches_played"] += period["statistics"]["matches_played"]
        overall_record["total_matches_won"] += period["statistics"]["matches_won"]

    return str(overall_record["total_matches_won"]) + " : " + str(overall_record["total_matches_played"] - overall_record["total_matches_won"])


def get_player_data(db: Session, player_id: str): 
    # create end point for request
    endPoint = f"{API_URL}{language}/competitors/{player_id}/profile.{format}?api_key={API_KEY}"
    
    response = requests.get(endPoint, headers=headers)
    
    # if the request is successful
    if response.status_code == 200:
        response = response.json()
        
        # map the api results to Player
        competitor_data = response.get('competitor', {})
        info_data = response.get('info', {})
        
        try:
            player_response = PlayerModel(
                id = str(competitor_data.get('id', '')),
                name = str(competitor_data.get('name', '')),
                weight = int(info_data.get('weight', 0)),
                height = int(info_data.get('height', 0)),
                nationality = str(competitor_data.get('country_code', 'NEU')),
                birthdate = info_data.get('date_of_birth'), # function to convert to date applied in model
                hand = 1 if str(info_data.get('handness', 'right')) == "right" else 2,
                biography = str(competitor_data.get('abbreviation', '')),
                coachid = 1,
                prizemoneywon = 500.0,
                gender = 1 if str(competitor_data.get('gender', 'male')) == "male" else 2,
                professionalrecord = "N/A", # calculate_overall_record(response.get('competitor_rankings', {})),
                mastersrecord = "N/A"
            )
            db.add(player_response)
            db.commit()
            db.refresh(player_response)
            return PlayerSchema.model_validate(player_response)
        
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Missing field in response: {e}")
    else:
        raise HTTPException(status_code=400, detail="Sport radar API call failed")