import pandas as pd
from typing import Union


DF_OR_LIST = Union[pd.DataFrame, list[dict]]

def write_to_csv(data: DF_OR_LIST, filepath: str) -> None:
    if type(data) is list:
        data = pd.DataFrame(data)
    data.to_csv(filepath, index=False)
    print(f"    Done writing data to {filepath}")
    
def read_all_from_csv() -> list[pd.DataFrame]:
    artists = pd.read_csv("app/data/artists.csv")
    albums = pd.read_csv("app/data/albums.csv")
    tracks = pd.read_csv("app/data/tracks.csv")
    track_features = pd.read_csv("app/data/track_features.csv")
    return artists, albums, tracks, track_features