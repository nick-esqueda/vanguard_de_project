import spotipy
import pandas as pd
import json
from typing import Iterable
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
def fetch_artists(urls: list[str]) -> dict:
    return (spot.artist(url) for url in urls)

# # take each artist URL and make a pruned version of the each artist.
# artists = fetch_artists(URLS)
# pruned_artists = prune_all(artists, "artist")

# artists_df = pd.DataFrame(pruned_artists)
# artists_df.to_csv("data/artists.csv")



# ALBUMS ---------------   
def fetch_artists_albums(urls: list[str]) -> list[dict]:
    """
    this function will take in 1 artist url, and fetch all of the artist's albums.
    then, it will prune each of those albums down and return an iterable of those albums.
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

# take each artist URL and make a pruned version of all of the albums for each.
albums = fetch_artists_albums(URLS)
all_pruned_albums = prune_all(albums, "album")

albums_df = pd.DataFrame(all_pruned_albums)
albums_df.to_csv("data/albums.csv") # send the albums DF to a .csv to temporarily cut down on queries during testing.



# ALBUM TRACKS ---------
def prune_track(track, album_id):
    pass

def fetch_and_prune_tracks(album_id: str) -> list[dict]:
    """
    this function will take in 1 album album_id, and fetch all of the album's songs.
    then, it will prune each of those songs down and return an iterable of those songs.
    """
    response = spot.album_tracks(album_id, limit=50, market="US")
    tracks = response["items"]
    offset = 0
    while response["next"]: # while there is a next page, request it, then add the new tracks from that new page.
        offset += 50
        response = spot.album_tracks(album_id, limit=50, offset=offset, market="US")
        tracks += response["items"]
        
    return [prune_track(track, album_id) for track in tracks] # [{}, {}, {}]
    
    
# albums_df = pd.read_csv("data/albums.csv")
# all_pruned_tracks = (track for id in albums_df["album_id"] for track in fetch_and_prune_tracks(id)) # nested generator comprehension to flatten the tracks to one level.
# tracks_df = pd.DataFrame(all_pruned_tracks)
# tracks_df.to_csv("data/tracks.csv")



# TRACK FEATURES -------
def prune_track_features(track):
    pass

def fetch_and_prune_track_features(track_ids):
    offset = 0
    track_features = []
    tracks = track_ids[0:100]
    while len(tracks) > 0: # change to "while track" and pass in an array for param?
        response = spot.audio_features(tracks=tracks) # [{}, {}, {}]
        track_features += response
        offset += 100
        tracks = track_ids[offset:offset + 100]
    
    # some tracks are coming back with None in the response, so need to filter those out.
    return [prune_track_features(track) for track in track_features if track is not None]
    

# tracks_df = pd.read_csv("data/tracks.csv")
# pruned_track_features = fetch_and_prune_track_features(tracks_df["track_id"])
# track_features_df = pd.DataFrame(pruned_track_features)
# track_features_df.to_csv("data/track_features.csv")