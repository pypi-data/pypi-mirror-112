from typing import Union
import numpy as np



def similarity(inp: str, original: str, ratio: bool = False) -> Union[float, int]:
    """
    Calculates how simliar 2 strings are
    This uses the levenshtein distance
    By default this return the amount
    of required edits to get the original string

    Parameter
    ---------
    inp : `str`
        The string you want to test
    original : `str`
        The original string
    ratio : `bool`
        Wheter to return the ratio instead of the edits
    """
    rows = len(inp) + 1
    cols = len(original) + 1
    distance = np.zeros((rows, cols), dtype=int)

    for i in range(1, rows):
        for k in range(1, cols):
            distance[i][0] = i
            distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if inp[row-1] == original[col-1]:
                cost = 0
            else:
                if ratio is True:
                    cost = 2
                else:
                    cost = 1
                
            distance[row][col] = min(
                distance[row-1][col] + 1,
                distance[row][col-1] + 1,
                distance[row-1][col-1] + cost
            )

    if ratio is True:
        r = ((len(inp) + len(original)) - distance[row][col]) / (len(inp) + len(original))
        return r
    else:
        return distance[row][col]