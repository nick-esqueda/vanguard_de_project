import pandas as pd


# READ IN DATA
artists = pd.read_csv("data/artists.csv")
albums = pd.read_csv("data/albums.csv")
tracks = pd.read_csv("data/tracks.csv")
track_features = pd.read_csv("data/track_features.csv")


# DROPPING UNNECESSARY COLUMNS
artists.drop(columns="Unnamed: 0", inplace=True)
albums.drop(columns="Unnamed: 0", inplace=True)
tracks.drop(columns="Unnamed: 0", inplace=True)
track_features.drop(columns="Unnamed: 0", inplace=True)


# FIXING DUPLICATES
albums.drop_duplicates(ignore_index=True, subset=["album_id"], inplace=True) # for duplicates from collaborations.
albums.drop_duplicates(ignore_index=True, subset=["album_name", "total_tracks", "artist_id"], inplace=True) # for duplicates of the same album, different "spotify version".
tracks.drop_duplicates(ignore_index=True, inplace=True)
track_features.drop_duplicates(ignore_index=True, inplace=True)

# remove the "appears_on" albums.
albums_filt = albums["album_group"] != "appears_on"
albums = albums[albums_filt]
albums.sort_index(ignore_index=True, inplace=True)

# remove all of the songs that aren't from the updated DataFrame of albums.
tracks_filt = tracks["album_id"].isin(albums["album_id"])
tracks = tracks[tracks_filt]
tracks.sort_index(ignore_index=True, inplace=True)

# grab all of the track_features that have a matching song in the updated tracks DataFrame.
track_feat_filt = track_features["track_id"].isin(tracks["track_id"])
track_features = track_features[track_feat_filt]
track_features.sort_index(ignore_index=True, inplace=True)


# print(albums)
# print(tracks)
# print(track_features)


def clean_artists(data):
    pass


def clean_albums(data):
    pass


def clean_tracks(data):
    pass


def clean_track_features(data):
    pass
    




def main():
    pass # run the main method of extract.py to get all the data so that you can transform it.


if __name__ == "__main__":
    main()