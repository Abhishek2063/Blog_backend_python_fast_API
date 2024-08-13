from fastapi import APIRouter
from controllers.comment_controller import router as comment_router
from utils.PrefixRouteList import COMMENT_API_PREFIX
from utils.TagsList import COMMENT_TAG

router = APIRouter()

# To create a user
router.include_router(comment_router, prefix=COMMENT_API_PREFIX, tags=[COMMENT_TAG])
