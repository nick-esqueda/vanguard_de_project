import spotipy
import pandas as pd
import json
from typing import Iterable, Generator
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from artist_urls import URLS
from utils.extract import prune_all
load_dotenv()


# API SETUP #####################################
auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)


# REQUESTS ######################################

# ARTISTS --------------
def fetch_artists(urls: Iterable[str]) -> Generator[dict]:
    """
    makes a call to the Spotify API to retrieve each artist's data from the passed in iterable. 
    returns a generator that returns each artist's data on each iteration. 
    """
    return (spot.artist(url) for url in urls)

# artists = fetch_artists(URLS)
# pruned_artists = prune_all(artists, "artist")

# artists_df = pd.DataFrame(pruned_artists)
# artists_df.to_csv("data/artists.csv")



# ALBUMS ---------------   
def fetch_artists_albums(urls: Iterable[str]) -> list[dict]:
    """
    fetches all of each artist's albums with each artist's url passed in as an iterable. 
    returns a list of those album's data from the Spotify API.
    """
    albums = [] # try not to use extra space! maybe map instead or something
    for url in urls:
        response = spot.artist_albums(url, limit=50, country="US")
        albums += response["items"]
        offset = 0
        while response["next"]: # while there is a next page, request it, then add the new albums from that new page.
            offset += 50
            response = spot.artist_albums(url, limit=50, offset=offset, country="US")
            albums += response["items"]
    return albums

# albums = fetch_artists_albums(URLS)
# all_pruned_albums = prune_all(albums, "album")

# albums_df = pd.DataFrame(all_pruned_albums)
# albums_df.to_csv("data/albums.csv") # send the albums DF to a .csv to temporarily cut down on queries during testing.



# ALBUM TRACKS ---------
def add_album_id(tracks: Iterable[dict], album_id: str) -> None:
    """
    mutates each of the given albums, adding an "album_id" key on it. 
    """
    for track in tracks: # put the album_id on each track.
        track["album_id"] = album_id

def fetch_tracks(album_ids: Iterable[str]) -> list[dict]:
    """
    takes in an iterable of album ids, and fetches every song for each of those albums from the Spotify API.
    returns a list of each song's data.
    """
    tracks = [] # try not to use extra space! maybe map instead or something
    for id in album_ids:
        response = spot.album_tracks(id, limit=50, market="US")
        add_album_id(response["items"], id)
        tracks += response["items"]
        
        offset = 0
        while response["next"]: # while there is a next page, request it, then add the new tracks from that new page.
            offset += 50
            response = spot.album_tracks(id, limit=50, offset=offset, market="US")
            add_album_id(response["items"], id)
            tracks += response["items"]
        
    return tracks
    
    
# albums_df = pd.read_csv("data/albums.csv")
# tracks = fetch_tracks(albums_df["album_id"])
# all_pruned_tracks = prune_all(tracks, "track")

# tracks_df = pd.DataFrame(all_pruned_tracks)
# tracks_df.to_csv("data/tracks.csv")



# TRACK FEATURES -------
def fetch_track_features(track_ids: Iterable[str]) -> list[dict]:
    """
    takes in an iterable of track ids and fetches each track's "track features" from the Spotify API. 
    returns a list of those track features for each track.
    """
    offset = 0
    track_features = []
    tracks = track_ids[0:100]
    while len(tracks) > 0:
        response = spot.audio_features(tracks=tracks)
        track_features += response
        offset += 100
        tracks = track_ids[offset:offset + 100]
    return track_features


# tracks_df = pd.read_csv("data/tracks.csv")
# track_features = fetch_track_features(tracks_df["track_id"])
# pruned_track_features = prune_all(track_features, "track_features")

# track_features_df = pd.DataFrame(pruned_track_features)
# track_features_df.to_csv("data/track_features.csv")
