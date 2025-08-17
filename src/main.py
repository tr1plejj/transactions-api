from fastapi import FastAPI

from src.routers import all_routers

app = FastAPI()

app.include_router(all_routers)
