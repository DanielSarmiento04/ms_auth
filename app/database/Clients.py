from . import __collection_client__
from ..models.Clients import (
    ClientInDB,
    Client
)


class ClientDB():

    @staticmethod
    def add_client_to_database(
        client: ClientInDB
    ):
        """
            This function receive the user_id and user Object and add the user in database
        """
        response = __collection_client__.insert_one(
            client.model_dump()
        )
        return response

    @staticmethod
    def get_client_from_database(
        client_id: str
    ) -> ClientInDB:
        """
            This function receive the client_id and return the user in database
        """
        client = __collection_client__.find_one(
            {"client_id": client_id}, {"_id": 0},)
        if not client:
            return None
        return ClientInDB(**client)

    @staticmethod
    def get_clients_from_database(
        client_id: str, 
        limit_registries: int = 10
    ) -> list[ClientInDB]:
        """
            This function receive the user_id and return the user in database
        """
        clients = __collection_client__.find({"client_id": client_id}, {
                                             "_id": 0}).limit(limit_registries)

        if not clients:
            return []

        return list(map(lambda client: ClientInDB(**client), clients))

    @staticmethod
    def delete_us_in_database(
        client_id: str
    ):
        """
            This function receive the user_id and delete the user in database
        """
        response = __collection_client__.delete_one({"client_id": client_id})
        return response
