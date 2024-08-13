from fastapi import APIRouter
from utils.PrefixRouteList import POST_API_PREFIX
from utils.TagsList import POST_TAG
from controllers.post_controller import router as post_router

router = APIRouter()

# To create a user
router.include_router(post_router, prefix=POST_API_PREFIX, tags=[POST_TAG])
