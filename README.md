# Blog Backend with FastAPI

This project is a backend service for a blog application, built using the FastAPI framework.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Blog Backend with FastAPI project provides a set of APIs to manage users, authentication, and user retrieval with sorting and pagination features. It serves as the backend for a blog application, handling user management and related functionalities.

## Features

- User creation
- User authentication
- Retrieving all users with sorting and pagination
- Retrieving user details by ID
- Update user details(first_name, last_name, role) By ID
- Update password 

## Installation

To set up the project locally, follow these steps:

### Clone the repository:

```bash
git clone https://github.com/Abhishek2063/Blog_backend_python_fast_API.git
cd Blog_backend_python_fast_API
```

### Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a .env file in the root directory of the project and add the following environment variables:

```bash
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
SECRET_KEY=<your_secret_key>
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

To run the application locally, use the following command:

```bash
uvicorn main:app --reload
The application will be accessible at http://127.0.0.1:8000.
```

## API Endpoints

Here are the available API endpoints:

### Create User

POST /api/user/create/

Request Body:

```bash
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123!",
    "role_id": 1
}
```

### User Login

POST /api/auth/login/

Request Body:

```bash
{
    "email": "john.doe@example.com",
    "password": "password123!"
}
```

### Get All Users

GET /api/user/get_all_users/

```bash
Query Parameters: sort_order, sort_by, skip, limit

Example: http://127.0.0.1:8000/api/user/get_all_users/?sort_order=asc&sort_by=email&skip=0&limit=10
```

### Get User by ID:

GET /api/user/{user_id}

```bash
Example: http://127.0.0.1:8000/api/user/get_user_by_id/1
```

### User Update By ID

PUT /api/user/update_user_details/{user_id}

Request Body:

```bash
{
    "first_name": "John",
    "last_name": "Doe",
    "role_id": 1
}
```

### User Update Password

PUT /api/user/update_user_password_details/{user_id}

Request Body:

```bash
{
    "current_password" : "Test#1234",
    "new_password" : "Test@1234"
}
```

## Dependencies

The project dependencies are listed in requirements.txt:

```bash
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
```

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
