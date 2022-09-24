import spotipy
import pandas as pd
import json
from typing import Iterable, Iterator, Literal
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from artist_urls import URLS
from utils.extract import prune_all, add_id
load_dotenv()


# API SETUP #####################################
auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)


# REQUESTS ######################################

# ARTISTS --------------
def fetch_artists(urls: Iterable[str]) -> Iterator[dict]:
    """
    makes a call to the Spotify API to retrieve each artist's data from the passed in iterable. 
    returns a iterator that returns each artist's data on each iteration. 
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
    albums = []
    for url in urls:
        id = url.split('/')[-1].split('?')[0]  
        
        response = spot.artist_albums(url, limit=50, country="US")
        add_id(response["items"], id, "artist_id")
        albums += response["items"]
        
        offset = 0
        while response["next"]: # while there is a next page, request it, then add the new albums from that new page.
            offset += 50
            response = spot.artist_albums(url, limit=50, offset=offset, country="US")
            add_id(response["items"], id, "artist_id")
            albums += response["items"]
            
    return albums

albums = fetch_artists_albums(URLS)
all_pruned_albums = prune_all(albums, "album")

albums_df = pd.DataFrame(all_pruned_albums)
albums_df.to_csv("data/albums.csv") # send the albums DF to a .csv to temporarily cut down on queries during testing.

# a = spot.artist_albums("https://open.spotify.com/artist/3YLUvWzk9eBm1WrHFlZxM4?si=DdbVig84TCOYOpfhzkvOTw", limit=50)
# print(json.dumps(a, indent=2))



# ALBUM TRACKS ---------
def fetch_tracks(album_ids: Iterable[str]) -> list[dict]:
    """
    takes in an iterable of album ids, and fetches every song for each of those albums from the Spotify API.
    returns a list of each song's data.
    """
    tracks = []
    for id in album_ids:
        response = spot.album_tracks(id, limit=50, market="US")
        add_id(response["items"], id, "album_id")
        tracks += response["items"]
        
        offset = 0
        while response["next"]: # while there is a next page, request it, then add the new tracks from that new page.
            offset += 50
            response = spot.album_tracks(id, limit=50, offset=offset, market="US")
            add_id(response["items"], id, "album_id")
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
