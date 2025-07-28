from pydantic import BaseModel
from typing import Optional

class Geolocation(BaseModel):
    lat: float
    lng: float

class Place(BaseModel):
    place_name: str
    owner_name: str
    address: str
    neighborhood: Optional[str] = None
    geolocation: Geolocation
    phone: Optional[str] = None
    email: Optional[str] = None
    activity: str