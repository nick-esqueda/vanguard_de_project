import pandas as pd
from .utils import DF_LIKE, to_df


# ARTISTS #######################################
@to_df
def clean_artists(artists: DF_LIKE) -> pd.DataFrame:
    """
    cleaning process:
    drop any rows with any null values from the given DataFrame.
    """
    artists.dropna(inplace=True)
    return artists

# ALBUMS ########################################
@to_df
def clean_albums(albums: DF_LIKE) -> pd.DataFrame:
    """
    cleaning process:
    drop any rows with nulls in any important columns.
    drop duplicates coming from collaborations between any of the artists.
    drop duplicates of the same album (different Spotify versions).
    drop any albums that are part of the "appears_on" album group (features).
    """
    albums.dropna(subset=["album_id", "album_name", "external_url", "album_uri", "artist_id"], inplace=True)
    albums.drop_duplicates(ignore_index=True, subset=["album_id"], inplace=True) 
    albums.drop_duplicates(ignore_index=True, subset=["album_name", "total_tracks", "artist_id"], inplace=True)
    
    filter = albums["album_group"] != "appears_on"
    albums = albums[filter]
    
    albums.sort_index(ignore_index=True, inplace=True)
    return albums

# TRACKS ########################################
@to_df
def clean_tracks(tracks: DF_LIKE, albums: DF_LIKE, artists: DF_LIKE) -> pd.DataFrame:
    """
    cleaning process:
    drop any rows with nulls in any important columns.
    drop any songs that aren't from an album in the the albums DataFrame.
    drop all single versions of tracks that are already on an existing album.
    """
    tracks.dropna(subset=["track_id", "song_name", "external_url", "song_uri", "album_id"], inplace=True)
    tracks.drop_duplicates(ignore_index=True, inplace=True)
    
    filter = tracks["album_id"].isin(albums["album_id"])
    tracks = tracks[filter]
    
    # find all single versions of album tracks.
    merged = tracks.merge(albums, on="album_id").merge(artists, on="artist_id")
    merged.sort_values(["album_group", "artist_name"], inplace=True) # to make sure the "album" type comes first.
    duped_filt = (merged.duplicated(subset=["artist_id", "song_name", "duration_ms"])) & (merged["album_group"] == "single")
    keep_ids = merged[~duped_filt]["track_id"] # this holds all of the track_ids that we want to keep.
    
    # remove those single versions.
    # NOTE: keep the "tracks" df and "merged" df separate since "merged" is sorted differently.
    filter = tracks["track_id"].isin(keep_ids)
    tracks = tracks[filter]
    
    tracks.sort_index(ignore_index=True, inplace=True)
    return tracks

# TRACK_FEATURES ################################
@to_df
def clean_track_features(track_features: DF_LIKE, tracks: DF_LIKE) -> pd.DataFrame:
    """
    cleaning process:
    drop rows with any null values.
    drop any duplicate rows.
    drop any rows that don't have a track in the tracks DataFrame.
    """
    track_features.dropna(inplace=True)
    track_features.drop_duplicates(ignore_index=True, inplace=True)
    
    filter = track_features["track_id"].isin(tracks["track_id"])
    track_features = track_features[filter]
    
    track_features.sort_index(ignore_index=True, inplace=True)
    return track_features
