from fastapi import FastAPI, status
from utils.response import create_response
from seedings.seed import seed_data
from routes.user_routes import router as user_router

seed_data()
app = FastAPI()


app.include_router(user_router)

@app.get("/")
def read_root():
    return create_response(status.HTTP_200_OK, True, "Welcome to Blogs API")

