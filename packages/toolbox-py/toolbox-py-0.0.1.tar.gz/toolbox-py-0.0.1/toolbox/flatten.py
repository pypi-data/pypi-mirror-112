from typing import List



def flatten(inp: List[list]) -> list:
    """
    Creates a single list out of a list of lists

    Parameters
    ----------
    inp : `list`
        The list of lists
    """
    return [i for sub in inp for i in sub]