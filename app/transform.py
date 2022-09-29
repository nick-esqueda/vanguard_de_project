import pandas as pd
from typing import Union


DF_OR_LIST = Union[pd.DataFrame, list[dict]]

# TRANSFORMATIONS ###############################
def clean_artists(artists: DF_OR_LIST) -> pd.DataFrame:
    if type(artists) is list:
        artists = pd.DataFrame(artists)
        
    artists.dropna(inplace=True)
    return artists

def clean_albums(albums: DF_OR_LIST) -> pd.DataFrame:
    if type(albums) is list:
        albums = pd.DataFrame(albums)
        
    albums.dropna(subset=["album_id", "album_name", "external_url", "album_uri", "artist_id"], inplace=True)
    
    # for duplicates from collaborations:
    albums.drop_duplicates(ignore_index=True, subset=["album_id"], inplace=True) 
    # for duplicates of the same album, but different "spotify version":
    albums.drop_duplicates(ignore_index=True, subset=["album_name", "total_tracks", "artist_id"], inplace=True)
    
    # remove all "appears_on" albums.
    filter = albums["album_group"] != "appears_on"
    albums = albums[filter]
    albums.sort_index(ignore_index=True, inplace=True)
    return albums

def clean_tracks(tracks: DF_OR_LIST, albums: DF_OR_LIST, artists: DF_OR_LIST) -> pd.DataFrame:
    if type(tracks) is list:
        tracks = pd.DataFrame(tracks)
    if type(albums) is list:
        albums = pd.DataFrame(albums)
    if type(artists) is list:
        artists = pd.DataFrame(artists)
    
    # drop any rows with any null values in the specified columns.
    tracks.dropna(subset=["track_id", "song_name", "external_url", "song_uri", "album_id"], inplace=True)
    tracks.drop_duplicates(ignore_index=True, inplace=True)
    
    # remove all songs that aren't from the updated DataFrame of albums.
    # this makes sure that all "appears_on" tracks are removed.
    filter = tracks["album_id"].isin(albums["album_id"])
    tracks = tracks[filter]
    
    # find all single versions of album tracks.
    merged = tracks.merge(albums, on="album_id").merge(artists, on="artist_id")
    merged.sort_values(["album_group", "artist_name"], inplace=True) # to make sure the "album" type comes first.
    duped = (merged.duplicated(subset=["artist_id", "song_name", "duration_ms"])) & (merged["album_group"] == "single")
    keep_ids = merged[~duped]["track_id"] # this holds all of the track_ids that you want to keep.
    
    # remove those single versions.
    # NOTE: keep the "tracks" df and "merged" df separate since "merged" is sorted differently.
    filter = tracks["track_id"].isin(keep_ids)
    tracks = tracks[filter]
    
    tracks.sort_index(ignore_index=True, inplace=True)
    return tracks

def clean_track_features(track_features: DF_OR_LIST, tracks: DF_OR_LIST) -> pd.DataFrame:
    if type(track_features) is list:
        track_features = pd.DataFrame(track_features)
    if type(tracks) is list:
        tracks = pd.DataFrame(tracks)
    
    track_features.dropna(inplace=True)
    track_features.drop_duplicates(ignore_index=True, inplace=True)
    
    # only include track_features for tracks that exist in the track DataFrame.
    filter = track_features["track_id"].isin(tracks["track_id"])
    track_features = track_features[filter]
    track_features.sort_index(ignore_index=True, inplace=True)
    return track_features
