from fastapi import APIRouter
from app.api.v1 import place

router = APIRouter()

router.include_router(place.router, prefix="/places", tags=["Places"])