from typing import TypeVar



_T = TypeVar("_T")


class Store(dict):
    """
    Represents a simple dict store

    Methods
    --------
    get()
        Gets a value based on the key 
    remove()
        Removes a key and its respective value
    set()
        Sets a key with the given value
    clear()
        Clears all items from the store
    all()
        Returns the entire store
    """
    def __init__(self):
        self.__dict__ = self


    def get(self, key):
        """
        Gets a value based on the key 
        """
        try:
            return self[key]
        except KeyError:
            return None

    
    def remove(self, key):
        """
        Removes a key and its respective value
        """
        try:
            del self[key]
        except KeyError:
            raise

    
    def set(self, key, value):
        """
        Sets a key with the given value
        """
        try:
            self[key] = value
        except KeyError:
            raise

    
    def clear(self):
        """
        Clears all items from the store
        """
        self.clear()


    def all(self):
        """
        Returns the entire store
        """
        return self


    def __len__(self):
        return len(self)