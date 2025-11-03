from fastapi import FastAPI
from src.routers import all_routers
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
app.include_router(all_routers)
Instrumentator().instrument(app).expose(app)
