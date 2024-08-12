from fastapi import APIRouter
from utils.PrefixRouteList import CATEGORY_API_PREFIX
from utils.TagsList import CATEGORY_TAG
from controllers.category_controller import router as category_router

router = APIRouter()

# To create a user
router.include_router(category_router, prefix=CATEGORY_API_PREFIX, tags=[CATEGORY_TAG])
