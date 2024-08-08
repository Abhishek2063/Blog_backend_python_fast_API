from fastapi import APIRouter
from controllers.auth_controller import router as auth_router

router = APIRouter()

# To login a user
router.include_router(auth_router, prefix="/api/auth", tags=["auth"])
