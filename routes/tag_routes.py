from fastapi import APIRouter
from utils.PrefixRouteList import TAG_API_PREFIX
from utils.TagsList import TAG_API_TAG
from controllers.tag_controller import router as tag_router

router = APIRouter()

# To create a user
router.include_router(tag_router, prefix=TAG_API_PREFIX, tags=[TAG_API_TAG])
