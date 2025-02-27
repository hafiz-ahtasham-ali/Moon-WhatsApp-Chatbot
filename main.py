from fastapi import FastAPI
from contextlib import asynccontextmanager
from models.database import create_tables
from controllers.whatsapp_controller import router as whatsapp_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()  # Create tables at startup
    yield  # Continue running the app

app = FastAPI(lifespan=lifespan)

app.include_router(whatsapp_router, prefix="/whatsapp", tags=["WhatsApp"])