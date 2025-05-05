<h1 align="center">
    Authorization Microservice
</h1>

<center>
    Jose Daniel Sarmiento , Manuel Ayala  | { jose2192232, jose2195529 } @correo.uis.edu.co
</center>

## Description

This microservice is responsible for managing the authentication and authorization of clients and users within the system. It provides endpoints to register clients, generate access tokens (JWT), and verify the validity of tokens. It also handles user registration, verification, and deletion.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ms_authorization
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    Create a `.env` file in the project root and define the necessary variables, such as `SECRET_KEY`.
    ```env
    SECRET_KEY='your_strong_secret_key_here'
    # Other configuration variables if any (e.g., Database URL)
    ```

## Running the Service

To start the Uvicorn development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The service will be available at `http://localhost:8000`. The interactive API documentation (Swagger UI) will be at `http://localhost:8000/docs`.

## API Endpoints

### Authentication and Clients (`/api/v1/Authorization`)

*   **`POST /Register`**: Registers a new client in the system.
    *   **Request Body:** `ClientInDB` (client\_id, password, state, role)
    *   **Response:** `ClientInDB` (with the hashed password)
*   **`POST /`**: Authenticates a client and generates a JWT access token.
    *   **Request Body:** `OAuth2PasswordRequestForm` (username=client\_id, password)
    *   **Response:** `{ "access_token": "...", "token_type": "bearer" }`
*   **`POST /Verify`**: Verifies if the access token provided in the `Authorization: Bearer <token>` header is valid. Requires authentication.
    *   **Response:** `200 OK` if the token is valid.

### User Management (`/user`)

*Note: All `/user` endpoints require a valid client token.*

*   **`GET /`**: Test endpoint to check connectivity.
*   **`POST /enrollment`**: Registers a new user.
    *   **Request Body:** `UserInDb` (username, password, role)
    *   **Response:** `User` (username, role)
*   **`GET /get_users_available`**: Retrieves the list of all registered users.
    *   **Response:** `list[User]`
*   **`POST /verify`**: Verifies a user's credentials (username and password).
    *   **Request Body:** `UserInDb` (username, password)
    *   **Response:** `UserInDb` if credentials are correct.
*   **`DELETE /delete?username={username}`**: Deletes a user by their username.
    *   **Response:** `200 OK` if deleted successfully.

