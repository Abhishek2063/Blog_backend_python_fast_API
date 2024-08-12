from fastapi import APIRouter
from controllers.role_controller import router as role_router
from utils.PrefixRouteList import USER_ROLE_API_PREFIX
from utils.TagsList import ROLE_TAG

router = APIRouter()

# To create a user
router.include_router(role_router, prefix=USER_ROLE_API_PREFIX, tags=[ROLE_TAG])
