# app/models/filters.py
from pydantic import BaseModel
from typing import Optional, Tuple

class PlaceFilter(BaseModel):
    search_mode: Optional[str] = None
    message: Optional[str] = None
    type_food: Optional[str] = None
    time_available: Optional[str] = None
    budget: Optional[str] = None
    quick_filter: Optional[str] = None
    coords: Optional[Tuple[float, float]] = None