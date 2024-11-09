from pydantic import BaseModel

class jsonResponse(BaseModel):
    message: str
    data: dict