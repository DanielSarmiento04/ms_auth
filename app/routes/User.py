from fastapi import (
    Depends, 
    APIRouter, 
    status, 
    HTTPException,
    Response
)

from datetime import timedelta

from ..models.User import (
    User,
    UserInDb
)

from .Clients import (
    Verify,
)

from ..dependencies import (
    get_current_client,
    AuthManager
)

from ..database.User import (
    UserDB
)

from colorama import Fore

router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Unprocessable Entity"},
        409: {"description": "Conflict"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal Server Error"},  
        503: {"description": "Service Unavailable"},
    },
    dependencies=[
        Depends(get_current_client)
    ]
)


@router.get(
    "/"
)
async def home():
    return {"message": "Hello, User!"}



@router.post(
    "/enrollment"
)
async def enrollment(
    user: UserInDb
) -> User:
    '''
        This function is used to register a new user

        Args:
            user: UserInDb - the user data to register

        Returns:
            UserInDb - the registered user
    '''
    print('User input:' + Fore.LIGHTBLUE_EX, user, Fore.RESET)

    user_db = UserDB.get_user_from_database(user.username)
    if user_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    user.password = AuthManager.get_password_hashed(user.password)
    UserDB.add_user_to_database(user)
    return User(
        username=user.username,
    )


@router.get(
    '/get_users_available'
)
async def get_user_available(
) -> list[User] :
    '''
        This function is used to return all users available 
    '''
    return UserDB.get_users_from_database()



@router.post(
    '/verify'
)
async def verify(
    user: UserInDb
) -> bool:
    '''
        This function is used to verify user in DB

        Args:
            user: UserInDb - the user data to verify
        
        Returns:
            UserInDb - the verified user
    '''

    user_from_db = UserDB.get_user_from_database(user.username)

    if not user_from_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        return AuthManager.verify_password(
            user.password,
            user_from_db.password,
        )
    
    except Exception as e:
        return False