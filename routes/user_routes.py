from fastapi import APIRouter
from controllers.user_controllers import router as user_router
from utils.TagsList import USER_TAG
from utils.PrefixRouteList import USER_API_PREFIX

router = APIRouter()

# To create a user
router.include_router(user_router, prefix=USER_API_PREFIX, tags=[USER_TAG])
