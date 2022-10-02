"""
this module holds functions that handle file input/output as well as manage
the transformation between different forms of data (mainly DataFrames/lists).

constants:
    DF_LIKE - a custom type for use in type hints.

functions:
    to_df - a decorator to convert function inputs to a DataFrame.
    write_to_csv - function to write the argument to a .csv file.
    read_all_from_csv - returns DataFrames of every .csv file.
"""

import pandas as pd
from typing import Any, Callable, Union


DF_LIKE = Union[pd.DataFrame, list[dict]]
        
def to_df(fn: Callable) -> Callable:
    """
    this is a decorator function that will convert the inputs of the decorated
    function to a pandas DataFrame.
    
    NOTE: all of the positional arguments of the original function
    must be DF_LIKE. kwargs can be used for any other arguments.
    """
    def wrapper(*args: DF_LIKE, **kwargs: Any) -> Any:
        args = (pd.DataFrame(arg) if type(arg) is not pd.DataFrame else arg 
                for arg in args)
        return fn(*args, **kwargs)
    return wrapper 

@to_df
def write_to_csv(data: DF_LIKE, filepath: str = "<unknown path>") -> None:
    """
    given a DF_LIKE object, this function will write that data to a .csv file
    in the given location.
    
    NOTE: "filepath=" is required.
    """
    data.to_csv(filepath, index=False)
    print(f"\tDone writing data to {filepath}")
    
def read_all_from_csv() -> list[pd.DataFrame]:
    """
    this function will read in each .csv file in app/data, convert to a
    DataFrame, and return them.
    if any of the .csv files are missing, an error message will be printed
    and None will be returned.
    """
    try:
        artists = pd.read_csv("app/data/artists.csv")
        albums = pd.read_csv("app/data/albums.csv")
        tracks = pd.read_csv("app/data/tracks.csv")
        track_features = pd.read_csv("app/data/track_features.csv")
        return artists, albums, tracks, track_features
    except FileNotFoundError:
        print("\nYou have not yet ran the program and chosen to write to .csv. Please run again.")
        return None
