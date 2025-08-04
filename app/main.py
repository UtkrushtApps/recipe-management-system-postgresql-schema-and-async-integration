from fastapi import FastAPI
from app.routes import api

app = FastAPI(title="Recipe Management API")
app.include_router(api.router)