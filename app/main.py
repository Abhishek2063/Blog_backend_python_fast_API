from fastapi import FastAPI, status, Request, HTTPException
from utils.response import create_response
from seedings.seed import seed_data
from routes.user_routes import router as user_router
from routes.auth_routes import router as auth_router
from routes.role_routes import router as role_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.messages import VALIDATION_ERROR, WELCOME_MESSAGE
from middlewares.custom_exception_handler import custom_http_exception_handler

seed_data()
app = FastAPI()

# Include custom exception handler
app.add_exception_handler(HTTPException, custom_http_exception_handler)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []

    for error in errors:
        formatted_errors.append({"field": error["loc"][-1], "message": error["msg"]})

    return JSONResponse(
        status_code=400,
        content={
            "status_code": 400,
            "success": False,
            "message": VALIDATION_ERROR,
            "errors": formatted_errors,
        },
    )


app.include_router(user_router)
app.include_router(auth_router)
app.include_router(role_router)


@app.get("/")
def read_root():
    return create_response(status.HTTP_200_OK, True, WELCOME_MESSAGE)
