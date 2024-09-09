from . import (
    __collection_users__
)
from ..models.User import (
    UserInDb,
    User
)


class UserDB():

    @staticmethod
    def add_user_to_database(user: UserInDb):
        """
            This function receive the user_id and user Object and add the user in database
        """
        response = __collection_users__.insert_one(
            user.model_dump()
        )
        return response
    
    @staticmethod
    def get_user_from_database(username:str) -> UserInDb | None:
        """
            This function receive the username and return the user in database
        """
        client = __collection_users__.find_one(
            {"username": username}, 
            {"_id": 0},
        )
        
        if not client:
            return None
        
        return UserInDb(**client)

    @staticmethod
    def get_users_from_database(limit_registries:int | None = None) -> list[UserInDb]:
        """
            This function receive the username and return the user in database

            Args:
                limit_registries (int, optional): The maximum number of users to return. Defaults to None.
        """
        users = __collection_users__.find(
            {},
            {"_id": 0}
        )

        if limit_registries != None:
            users = users.limit(limit_registries)

        if not users:
            return []
        
        return list(
            map(
                lambda user: UserInDb(**user), 
                users
            )
        )

    @staticmethod
    def delete_users_in_database(username:str):
        """
            This function receive the username and delete the user in database
        """
        response = __collection_users__.delete_one(
            {"username": username}
        )
        return response
    