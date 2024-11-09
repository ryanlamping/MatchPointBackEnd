from pydantic import BaseModel
from typing import Optional, List

class Competitor(BaseModel):
    id: str = None
    name: str = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    abbreviation: Optional[str] = None

class CompetitorRanking(BaseModel):
    rank: int = None
    movement: int = None
    points: int = None
    competitions_played: int = None
    competitor: Competitor = None

class Ranking(BaseModel):
    type_id: int = None
    name: str = None
    year: int = None
    week: int = None
    gender: str = None
    competitor_rankings: List[CompetitorRanking] = None

class RankingsResponse(BaseModel):
    generated_at: str = None
    rankings: Optional[List[Ranking]] = None
    message: Optional[str] = None # Fast api requires