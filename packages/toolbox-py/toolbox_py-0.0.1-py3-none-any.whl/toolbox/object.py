



class S:
    """
    Gets all keys from a dict and adds them 
    as attribute to a class (also works with nested dicts)

    Parameters
    ----------
    data : ``dict`
        The dict you want to convert
    """
    def __init__(self, data: dict) -> None:
        self.__raw = data
        class _(dict):
            def __init__(self, *args, **kwargs):
                super(_, self).__init__(*args, **kwargs)
                self.__dict__ = self
            
            @classmethod
            def nested(cls, data):
                if not isinstance(data, dict):
                    return data
                else:
                    return cls({k: cls.nested(data[k]) for k in data})

        for k, v in _.nested(data).items():
            setattr(self, k, v)
    

    def __len__(self) -> int:
        print([x for x in dir(self) if not x.startswith("_")])
        return len([x for x in dir(self) if not x.startswith("_")])
    

    def __repr__(self) -> str:
        return "<class 'S'>"
    

    def _new(self, new=None) -> None:
        """
        Renews the data
        """
        self.__init__(new or self.__raw)