# Future Furniture Backend

A FastAPI backend for a furniture design application with authentication and role-based access control.

## Features

- User authentication with JWT tokens and cookies
- Role-based access control (designer and customer roles)
- MongoDB integration
- RESTful API endpoints for user and design management

## Requirements

- Python 3.8+
- MongoDB

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/future-furniture-backend.git
    cd future-furniture-backend
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Make sure MongoDB is running on your system.

## Configuration

Before running the application, you should update the following settings in `app/utils/auth.py`:

- `SECRET_KEY`: Change to a secure random string
- In production, set `secure=True` for cookies

## Running the Application

Start the application with:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /signup`: Register a new user
- `POST /login`: Authenticate and get access token
- `POST /logout`: Logout and clear cookie

### Designs

- `GET /getAllDesigns`: Get all designs (all authenticated users)
- `GET /getUserDesigns`: Get designs owned by the current user (designers only)
- `POST /createDesign`: Create a new design (designers only)
- `PUT /updateDesign/{design_id}`: Update a design (designers who own the design)
- `DELETE /deleteDesign/{design_id}`: Delete a design (designers who own the design)

## Data Models

### User

```json
{
  "username": "string",
  "name": "string",
  "role": "designer"
}
```

### Design

```json lines
{
  "id": "string",
  "ownerId": "string",
  "name": "string",
  "data": {}
  // Arbitrary JSON data
}
```

## Security

- Passwords are hashed using bcrypt
- Authentication is handled via JWT tokens
- Tokens are stored in HTTP-only cookies for XSS protection
- Role-based access control for all endpoints