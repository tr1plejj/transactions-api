from fastapi import APIRouter
from .user_router import router as user_router
from .admin_router import router as admin_router
from .transaction_router import router as transaction_router

all_routers = APIRouter()
router_list = [user_router, admin_router, transaction_router]

for router in router_list:
    all_routers.include_router(router)
