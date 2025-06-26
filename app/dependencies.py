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
from typing import Optional

# Internals DTO'S schemas
from .models.Clients import (
    Client,
    ClientInDB
)

from .database.Clients import ClientDB
from .constants import SECRET_KEY

# --- Constants ---
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12  # 12 hours

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

    ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

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
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
            Description
            -----------
            Create the access token using Jose with HS256
        """
        to_encode = data.copy()
        # Create per default a token that expires based on ACCESS_TOKEN_EXPIRE_MINUTES
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            # Use the module-level constant
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        # Use class-level access for constants
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt


async def get_current_client(token: str = Depends(oauth2_scheme)):
    '''
        This function is used to validate the token in the security zone, if the token is valid then return the user
        Args:
            token: str - the token to validate
        Returns:
            ClientInDB - the Client that the token belongs
    '''
    try:
        # Use constants directly
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        client_id: str = payload.get("sub")
        if client_id is None:
            raise credentials_exception
        token_data = TokenData(username=client_id)
    except JWTError:
        raise credentials_exception
    # Use the modified get_existing_client
    user = get_existing_client(token_data.username)
    if not user:
        # If user not found after decoding token, raise credentials exception
        raise credentials_exception
    return user


def get_existing_client(client_id: str) -> Optional[ClientInDB]:
    '''
        Description
        -----------
        This function is used to get a client from the database.

        Parameters
        ----------
        client_id: str

        Returns
        -------
        Optional[ClientInDB]: The client if found, otherwise None.
    '''
    client = ClientDB.get_client_from_database(client_id)
    # Return the client object or None, let the caller handle the case where client is None
    return client

