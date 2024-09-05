from fastapi import (
    Depends, 
    APIRouter, 
    status, 
    HTTPException,
    Response
)

from ..dependencies import (
    OAuth2PasswordRequestForm, 
    AuthManager, 
    get_existing_client,
    get_current_client
)

from datetime import timedelta
from ..models.Clients import (
    Client,
    ClientInDB 
)

from ..database.Clients import (
    ClientDB
)

router = APIRouter(
    prefix="/api/v1/Authorization",
    tags=["client"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "Conflict"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal Server Error"},  
        503: {"description": "Service Unavailable"},
    }
)

no_authenticate_client_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Client not authenticated",
    headers={"Content-Type": "application/json"},
)

def authenticate_client(client_id: str, password: str):
    '''
        Function to validate the user and password with the registered in database

        Args: 
            client_id: str - the id of the user
            password: str - the password of the user
    '''

    client = get_existing_client(client_id)

    print(client)
    # If the client doesn't exist in database 
    if not client:
        return False
    
    # If the password doesn't match with the registered in database
    if not AuthManager.verify_password(password, client.password):
        return False
    
    return client

@router.post("/Register")
async def register(client: ClientInDB):
    '''
        Function to register a new client in the database

        Args: 
            client: ClientInDB - the client to register

                - client_id: The ID of the client
                - password: The password of the client
                - state: The state of the client
                - role: The role of the client

        Returns:
            ClientInDB - the client registered
    
    '''
    client_db = ClientDB.get_client_from_database(client.client_id)

    if client_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Client already registered",
            headers={"Content-Type": "application/json"},
        )
    
    # Hash the password
    password_hashed = AuthManager.get_password_hashed(client.password)
    client.password = password_hashed

    ClientDB.add_client_to_database(client)
    return client

@router.post("/")
async def authorization(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
        This function is used to generate a OAuth2 token for the user

        Args:
            form_data: OAuth2PasswordRequestForm - the form data with the user and password
                - username
                - password
        Returns:
            dict - the token generated
    '''
    client = authenticate_client(form_data.username, form_data.password)

    if not client:
        raise no_authenticate_client_exception

    access_token_expires = timedelta(minutes=AuthManager.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthManager.create_access_token(
        data={"sub": form_data.username, "role": client.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/Verify", dependencies=[Depends(get_current_client)])
async def Verify():
    '''
        This function is used to verify if the user is authenticated

        Returns:
            Response - the response with the status code 200
    '''
    return Response(status_code=status.HTTP_200_OK)
   