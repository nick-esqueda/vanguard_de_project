import pandas as pd
from utils import read_all_from_csv
import extract


# TRANSFORMATIONS ###############################
def clean_artists(artists: pd.DataFrame) -> pd.DataFrame:
    artists.dropna(inplace=True)
    return artists

def clean_albums(albums: pd.DataFrame) -> pd.DataFrame:
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

def clean_tracks(tracks: pd.DataFrame, albums: pd.DataFrame, artists: pd.DataFrame) -> pd.DataFrame:
    tracks.dropna(subset=["track_id", "song_name", "external_url", "song_uri", "album_id"], inplace=True)
    tracks.drop_duplicates(ignore_index=True, inplace=True)
    
    # remove all songs that aren't from the updated DataFrame of albums.
    # this makes sure that all "appears_on" tracks are removed.
    filter = tracks["album_id"].isin(albums["album_id"])
    tracks = tracks[filter]
    
    # find all single versions of album tracks and remove them.
    merged = tracks.merge(albums, on="album_id").merge(artists, on="artist_id")
    merged.sort_values(["album_group", "artist_name"], inplace=True) # to make sure the "album" type comes first.
    
    duped = (merged.duplicated(subset=["artist_id", "song_name", "duration_ms"])) & (merged["album_group"] == "single")
    keep_ids = merged[~duped]["track_id"] # this holds all of the track_ids that you want to keep.
    
    # NOTE: keep the "tracks" df and "merged" df separate since "merged" is sorted differently.
    filter = tracks["track_id"].isin(keep_ids)
    tracks = tracks[filter]
    
    tracks.sort_index(ignore_index=True, inplace=True)
    return tracks

def clean_track_features(track_features: pd.DataFrame, tracks: pd.DataFrame) -> pd.DataFrame:
    track_features.dropna(inplace=True)
    track_features.drop_duplicates(ignore_index=True, inplace=True)
    
    # only include track_features for tracks that exist in the track DataFrame.
    filter = track_features["track_id"].isin(tracks["track_id"])
    track_features = track_features[filter]
    track_features.sort_index(ignore_index=True, inplace=True)
    return track_features
    
def print_transformations(artists, albums, tracks, track_features):
    print("\nARTISTS:")
    print(artists)
    print("\nALBUMS:")
    print(albums)
    print("\nTRACKS:")
    print(tracks)
    print("\nTRACK_FEATURES:")
    print(track_features)
    
    
# MAIN ###################################################################
##########################################################################
def main():
    # # fetch all of the data first.
    # artists, albums, tracks, track_features = (pd.DataFrame(data) for data in extract.main())
    
    # OPTIONAL: use data from .csv instead of extracting everything again.
    artists, albums, tracks, track_features = read_all_from_csv()
    
    # clean the extracted data.
    artists = clean_artists(artists)
    albums = clean_albums(albums)
    tracks = clean_tracks(tracks, albums, artists)
    track_features = clean_track_features(track_features, tracks)
    
    # print_transformations(artists, albums, tracks, track_features)
    
    print("Done cleaning all data!")
    return artists, albums, tracks, track_features


if __name__ == "__main__":
    main()