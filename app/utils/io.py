import pandas as pd
from typing import Any, Callable, Union


DF_LIKE = Union[pd.DataFrame, list[dict]]
        
def to_df(fn: Callable) -> Callable:
    def wrapper(*args: DF_LIKE, **kwargs: Any) -> Any:
        args = (pd.DataFrame(arg) for arg in args if type(arg) is not pd.DataFrame)
        return fn(*args, **kwargs)
    return wrapper 

@to_df
def write_to_csv(data: DF_LIKE, filepath: str = "<unknown path>") -> None:
    data.to_csv(filepath, index=False)
    print(f"\tDone writing data to {filepath}")
    
def read_all_from_csv() -> list[pd.DataFrame]:
    try:
        artists = pd.read_csv("app/data/artists.csv")
        albums = pd.read_csv("app/data/albums.csv")
        tracks = pd.read_csv("app/data/tracks.csv")
        track_features = pd.read_csv("app/data/track_features.csv")
        return artists, albums, tracks, track_features
    except FileNotFoundError:
        print("\nYou have not yet ran the program and chosen to write to .csv. Please run again.")
