import pandas as pd
from typing import Union


def write_to_csv(data: Union[list[dict], pd.DataFrame], filepath: str) -> None:
    if type(data) is not pd.DataFrame:
        data = pd.DataFrame(data)
    data.to_csv(filepath, index=False)
    print(f"    Done writing data to {filepath}")
    
def read_all_from_csv() -> list[pd.DataFrame]:
    artists = pd.read_csv("data/artists.csv")
    albums = pd.read_csv("data/albums.csv")
    tracks = pd.read_csv("data/tracks.csv")
    track_features = pd.read_csv("data/track_features.csv")
    return artists, albums, tracks, track_features