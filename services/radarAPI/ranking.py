from fastapi import HTTPException
import requests
from core.config import settings
from models.rankings import RankingsResponse, Ranking, CompetitorRanking, Competitor

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

# function to hit end point
def get_rankings(language: str):
    # create end point for request
    language = "en"
    endPoint = f"{API_URL}{language}/rankings.{format}?api_key={API_KEY}"
    
    response = requests.get(endPoint, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        
        # map the api results to RankingsResponse
        try:
            rankings_response = RankingsResponse(
                generated_at=response_data["generated_at"],
                rankings=[
                    Ranking(
                        type_id=r["type_id"],
                        name=r["name"],
                        year=r["year"],
                        week=r["week"],
                        gender=r["gender"],
                        competitor_rankings=[
                            CompetitorRanking(
                                rank=c["rank"],
                                movement=c.get("movement", 0),
                                points=c["points"],
                                competitions_played=c["competitions_played"],
                                competitor=Competitor(
                                    id=c["competitor"]["id"],
                                    name=c["competitor"]["name"],
                                    country=c.get("competitor", {}).get("country", ""),
                                    country_code=c.get("competitor", {}).get("country_code", " "), 
                                    abbreviation=c.get("competitor", {}).get("abbreviation", " ")
                                )
                            ) for c in r["competitor_rankings"]
                        ]
                    ) for r in response_data["rankings"]
                ]
            )
            return rankings_response
        
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Missing field in response: {e}")
    else:
        raise HTTPException(status_code=400, detail="Sport radar API call failed")