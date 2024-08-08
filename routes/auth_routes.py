from fastapi import APIRouter
from controllers.auth_controller import router as auth_router
from utils.PrefixRouteList import AUTH_API_PREFIX
from utils.TagsList import AUTH_TAG

router = APIRouter()

# To login a user
router.include_router(auth_router, prefix=AUTH_API_PREFIX, tags=[AUTH_TAG])
