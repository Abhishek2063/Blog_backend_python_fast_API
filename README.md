# Blog Backend with FastAPI

Welcome to the Blog Backend project built with FastAPI. This project provides a set of APIs to manage users, authentication, and user retrieval with sorting and pagination features.

## GitHub Repository

The source code for this project is available on GitHub: [Blog Backend with FastAPI](https://github.com/Abhishek2063/Blog_backend_python_fast_API.git)

## Table of Contents

- [Project Overview](#project-overview)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)

## Project Overview

This project is a backend service for a blog application. It includes the following functionalities:
- User creation
- User authentication
- Retrieving all users with sorting and pagination

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/Abhishek2063/Blog_backend_python_fast_API.git
    cd Blog_backend_python_fast_API
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=<your_secret_key>
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

Running the Application
To run the application locally, use the following command:

uvicorn main:app --reload

The application will be accessible at http://127.0.0.1:8000.

API Endpoints
Here are the available API endpoints:

Create User: POST /api/user/create/

Request Body:
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123!",
    "role_id": 1
}


User Login: POST /api/auth/login/

Request Body:
{
    "email": "john.doe@example.com",
    "password": "password123!"
}

Get All Users: GET /api/user/get_all_users/

Query Parameters: sort_order, sort_by, skip, limit
Example: http://127.0.0.1:8000/api/user/get_all_users/?sort_order=asc&sort_by=email&skip=0&limit=10


Dependencies

The project dependencies are listed in requirements.txt:

css
Copy code
fastapi
uvicorn
sqlalchemy
pymysql
pydantic
bcrypt==4.0.1
passlib[bcrypt]
python-jose
python-dotenv
python-multipart
passlib
pydantic[email]

Feel free to explore the source code and contribute to the project!





