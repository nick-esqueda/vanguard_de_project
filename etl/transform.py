import pandas as pd


# READ IN DATA
artists = pd.read_csv("data/artists.csv")
albums = pd.read_csv("data/albums.csv")
tracks = pd.read_csv("data/tracks.csv")
track_features = pd.read_csv("data/track_features.csv")


def clean_artists(artists):
    pass

def clean_albums(albums):
    # for duplicates from collaborations:
    albums.drop_duplicates(ignore_index=True, subset=["album_id"], inplace=True) 
    # for duplicates of the same album, different "spotify version":
    albums.drop_duplicates(ignore_index=True, subset=["album_name", "total_tracks", "artist_id"], inplace=True)
    
    # remove all "appears_on" albums.
    filter = albums["album_group"] != "appears_on"
    albums = albums[filter]
    albums.sort_index(ignore_index=True, inplace=True)
    return albums

def clean_tracks(tracks, albums):
    tracks.drop_duplicates(ignore_index=True, inplace=True)
    
    # remove all songs that aren't from the updated DataFrame of albums.
    # (this makes sure that all "appears_on" tracks are removed.)
    filter = tracks["album_id"].isin(albums["album_id"])
    tracks = tracks[filter]
    tracks.sort_index(ignore_index=True, inplace=True)
    return tracks

def clean_track_features(track_features, tracks):
    track_features.drop_duplicates(ignore_index=True, inplace=True)
    
    # only include track_features for tracks that exist in the track DataFrame.
    filter = track_features["track_id"].isin(tracks["track_id"])
    track_features = track_features[filter]
    track_features.sort_index(ignore_index=True, inplace=True)
    return track_features
    



#################################################
def main():
    artists = clean_artists(artists)
    albums = clean_albums(albums)
    tracks = clean_tracks(tracks, albums)
    track_features = clean_track_features(track_features, tracks)


if __name__ == "__main__":
    main()