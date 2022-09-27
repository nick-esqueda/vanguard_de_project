import pandas as pd
import extract
from utils.artist_urls import ARTIST_URLS


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

def clean_tracks(tracks: pd.DataFrame, albums: pd.DataFrame) -> pd.DataFrame:
    tracks.dropna(subset=["track_id", "song_name", "external_url", "song_uri", "album_id"], inplace=True)
    tracks.drop_duplicates(ignore_index=True, inplace=True)
    
    # remove all songs that aren't from the updated DataFrame of albums.
    # (this makes sure that all "appears_on" tracks are removed.)
    filter = tracks["album_id"].isin(albums["album_id"])
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
    



#################################################
def main():
    # # fetch all of the data first.
    # artists, albums, tracks, track_features = extract.main()
    
    # OPTIONAL: use data from .csv instead of fetching everything again.
    artists = pd.read_csv("data/artists.csv")
    albums = pd.read_csv("data/albums.csv")
    tracks = pd.read_csv("data/tracks.csv")
    track_features = pd.read_csv("data/track_features.csv")
    
    # clean the extracted data.
    artists = clean_artists(pd.DataFrame(artists))
    albums = clean_albums(pd.DataFrame(albums))
    tracks = clean_tracks(pd.DataFrame(tracks), pd.DataFrame(albums))
    track_features = clean_track_features(pd.DataFrame(track_features), pd.DataFrame(tracks))
    
    # print("\nARTISTS:")
    # print(artists)
    # print("\nALBUMS:")
    # print(albums)
    # print("\nTRACKS:")
    # print(tracks)
    # print("\nTRACK_FEATURES:")
    # print(track_features)
    
    return artists, albums, tracks, track_features


if __name__ == "__main__":
    main()