
# FastApi Security Schema, DTO'S and toolkit necessary to manage the authentication
from fastapi import (
    HTTPException, 
    Depends, 
    status
)
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm
)
# Python jose cryptography 
from jose import (
    JWTError, 
    jwt
)

# Cryptography
from passlib.context import CryptContext
from datetime import (
    datetime, 
    timedelta
)
from pydantic import BaseModel

# Internals DTO'S schemas
from .models.Clients import (
    Client,
    ClientInDB
)

from .database.Clients import ClientDB
from .exceptions import NoFoundException
from .constants import SECRET_KEY

# Logs
from colorama import Fore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/Authorization")

__pwd_context__ = CryptContext(schemes=["bcrypt"], deprecated="auto")

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None

class AuthManager():
    
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12  # minutes
    SECRET_KEY = SECRET_KEY

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
            Description
            -----------
            Verify if the password is correct using PassLib with Bcrypt
        """
        return __pwd_context__.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hashed(password):
        """
            Description
            -----------
            Hash the password using PassLib with Bcrypt
        """
        return __pwd_context__.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None= None) -> str:
        """
            Description
            -----------
            Create the access token using Jose with HS256
        """
        to_encode = data.copy()
        # Create per default a token that expire in 15 minutes
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthManager().SECRET_KEY, algorithm = AuthManager().ALGORITHM)
        
        return encoded_jwt



async def get_current_client(token: str = Depends(oauth2_scheme)):
    '''
        This function is used to validate the token in the security zone, if the token is valid then return the user
        Args:
            token: str - the token to validate
        Returns:
            Client - the Client that the token belongs
    '''
    try:
        payload = jwt.decode(token, AuthManager.SECRET_KEY, algorithms=[AuthManager.ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        token_data = TokenData(username=client_id)
        # print(token_data)
    except JWTError:
        raise credentials_exception
    user = get_existing_client(token_data.username)
    if not  user:
        raise credentials_exception
    return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail="Inactive user",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )   
#     return current_user

# def get_existing_user(user_id: str) -> UserInDB:
#     """
#         Description
#         -----------
#         This function is used to get a user from the database.
        
#         Parameters
#         ----------
#         user_id: str
        
#         Returns
#         -------
#         User
#     """
#     user = UserDB.get_user_from_database(user_id)
#     print('User in database:' + Fore.LIGHTBLUE_EX, user)
#     if not user:
#         raise NoFoundException(user_id=user_id, context="User")
#     return user

def get_existing_client(client_id: str) -> ClientInDB:
    '''
        Description
        -----------
        This function is used to get a client from the database.
        
        Parameters
        ----------
        client_id: str
        
        Returns
        -------
        Client
    '''
    client = ClientDB.get_client_from_database(client_id)
    print('Client in database:' + Fore.LIGHTBLUE_EX, client)
    if not client:
        raise NoFoundException(user_id=client_id, context="User")
    return client   

# def update_user_password(user_id: str, reqUser: UserPass) -> bool:
#     """
#         Description
#         -----------
#         This function is used to update a user password from the database.
        
#         Parameters
#         ----------
#         user_id: str
        
#         Returns
#         -------
#         User
#     """
#     res = UserDB.update_user_password(user_id, reqUser)
#     return res

# def update_user(user_id: str, reqUser: User) -> bool:
#     """
#         Description
#         -----------
#         This function is used to update a user from the database.
        
#         Parameters
#         ----------
#         user_id: str
        
#         Returns
#         -------
#         User
#     """
#     res = UserDB.update_user_password(user_id, reqUser)
#     return res