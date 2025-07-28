from app.models.place_filters import PlaceFilter
from app.repositories.place_repository import get_all_places

def get_recommendations(filters: PlaceFilter):
    all_places = get_all_places(filters)
    return all_places[:10]
