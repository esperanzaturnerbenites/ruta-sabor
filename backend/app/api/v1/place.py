from fastapi import APIRouter, Query

from app.models.place import Place
from app.models.place_filters import PlaceFilter

from app.services import place

from typing import List

router = APIRouter()

@router.get("/recommendations", response_model=List[Place])
async def get_recommendations(
    search_mode: str | None = Query(None),
    message: str | None = Query(None),
    type_food: str | None = Query(None),
    time_available: str | None = Query(None),
    budget: str | None = Query(None),
    quick_filter: str | None = Query(None),
    coords: str | None = Query(None)
):
    coords_tuple = None
    if coords:
        try:
            lat, lng = map(float, coords.split(","))
            coords_tuple = (lat, lng)
        except ValueError:
            pass

    filters = PlaceFilter(
        search_mode=search_mode,
        message=message,
        type_food=type_food,
        time_available=time_available,
        budget=budget,
        quick_filter=quick_filter,
        coords=coords_tuple
    )

    return place.get_recommendations(filters)