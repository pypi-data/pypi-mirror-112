
import string
import unidecode



def asciify(text: str) -> str:
    """
    Removes all non-ascii chars from a string

    Parameter
    ---------
    text : `str`
        The string you want to modify
    """
    return "".join(
        filter(
            lambda x: x in list(string.ascii_letters) or x.isspace(), 
            unidecode.unidecode(text).lower()
        )
    )