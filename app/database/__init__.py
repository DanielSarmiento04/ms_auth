from pymongo import MongoClient
from ..constants import (
    __url_client__,
    __name_database__
)

__client__ = MongoClient(__url_client__)
__database__ = __client__[__name_database__]

__collection_users__ = __database__["users"]
__collection_client__ = __database__["clients"]
