from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="La Ruta del Sabor",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://rutadelsaborgirardot.netlify.app",
        "https://ruta-sabor-girardot-dev.loca.lt"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)