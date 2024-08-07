from fastapi import FastAPI, status
from utils.response import create_response
from seedings.seed import seed_data

seed_data()
app = FastAPI()


@app.get("/")
def read_root():
    return create_response(status.HTTP_200_OK, True, "Welcome to Blogs API")
