from fastapi import APIRouter
from controllers.user_controllers import router as user_router

router = APIRouter()

# To create a user
router.include_router(user_router, prefix="/api/user", tags=["users"])
