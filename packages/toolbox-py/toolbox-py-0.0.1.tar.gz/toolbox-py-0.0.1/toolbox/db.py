from pymongo import MongoClient
from pymongo.collection import Collection as MongoCollection
from pymongo.database import Database as MongoDatabase

from typing import TypeVar, Union



_T = TypeVar("_T")


class Collection(MongoCollection):
    """
    Respresents a collection subclassed from `Collection`

    Parameters
    ----------
    database : `Database`
        The database this collection belongs to
    name : `str`
        The name of the collection

    Attributes
    ----------
    key : `str`
        The key to fetch documents by, this should always be 'id'

    Methods
    ----------
    get()
        Get a value from the colleciton
    insert()
        Inserts a document
    update()
        Updates the given key in the collection
    delete()
        Deletes a document
    exists()
        Checks wheter or not a document exists
    get_doc()
        Fetches the entire doument based on the key
    """
    def __init__(self, database: MongoDatabase, name: str, **kwargs) -> None:
        super().__init__(database, name, **kwargs)
        self.key = "id"


    def get(self, filter_value: _T, key: _T) -> Union[_T, None]:
        """
        Get a value from the colleciton
        """
        if isinstance(filter_value, int):
            filter_value = str(filter_value)
        try:
            for _ in super().find({f"{self.key}": f"{filter_value}"}):
                return _[f"{key}"]
        except Exception:
            return None


    def insert(self, schema: dict) -> None:
        """
        Inserts a document
        """
        super().insert_one(schema)

    
    def update(self, filter_value: _T, key: _T, new_value: _T) -> None:
        """
        Updates the given key in the collection
        """
        super().update({f"{self.key}": f"{filter_value}"}, {"$set": {f"{key}": new_value}}, upsert=False, multi=False)

    
    def delete(self, filter_value: _T):
        """
        Deletes a document
        """
        super().delete_one({f"{self.key}": f"{filter_value}"})


    def exists(self, filter_value: _T) -> bool:
        """
        Checks wheter or not a document exists
        """
        found = [x for x in super().find({f"{self.key}": f"{filter_value}"})]
        if len(found) <= 0 or found == "":
            return False
        else:
            return True


    def get_doc(self, filter_value: _T) -> Union[_T, None]:
        """
        Fetches the entire doument based on the key
        """
        try:
            return list(super().find({f"{self.key}": f"{filter_value}"}))[0]
        except Exception:
            return None


class _Database(MongoDatabase):
    """
    Represent a Database, subclassed from `Database`

    Parameters
    ----------
    client : `Client`
        The MongoClient this database belongs to
    name : `str` 
        The name of the database
    """
    def __init__(self, client: MongoClient, name: str, **kwargs) -> None:
        super().__init__(client, name, **kwargs)


class Database(_Database):
    """
    Represents the actual Database used in 
    the code, subclassed from `MongoClient`

    Parameters
    ----------
    name : `str`
        Name of the main database
    host : `str`
        The MongoURL/host
    port : `int`
        The port to use, None to use default one
    """
    def __init__(self, name: str, host: str, port : int = None, **kwargs) -> None:
        super().__init__(client=MongoClient(host=host, port=port, **kwargs), name=name)
