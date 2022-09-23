import spotipy
import pandas as pd
import json
from typing import Iterable
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from artist_urls import URLS
load_dotenv()


# API SETUP #####################################
auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)


# REQUESTS ######################################

# ARTISTS --------------
def fetch_and_prune_artist(url: str) -> dict:
    artist = spot.artist(url)
    return {
        "artist_id": artist["id"],
        "artist_name": artist["name"],
        "external_url": artist["external_urls"]["spotify"],
        "genre": artist["genres"][0],
        "image_url": artist["images"][0]["url"],
        "followers": artist["followers"]["total"],
        "popularity": artist["popularity"],
        "type": artist["type"],
        "artist_uri": artist["uri"]
    }

    
# # take each artist URL and make a pruned version of the each artist.
# pruned_artists = map(lambda url: fetch_and_prune_artist(url), URLS)
# artists_df = pd.DataFrame(pruned_artists)
# artists_df.to_csv("data/artists.csv")


# ALBUMS ---------------
def prune_album(album):
    return {
        "album_id": album["id"],
        "album_name": album["name"],
        "external_url": album["external_urls"]["spotify"],
        "image_url": album["images"][0]["url"],
        "release_date": album["release_date"],
        "total_tracks": album["total_tracks"],
        "type": album["type"],
        "album_uri": album["uri"],
        "artist_id": album["artists"][0]["id"]
    }
    
def fetch_and_prune_albums(url: str) -> list[dict]:
    """
    this function will take in 1 artist url, and fetch all of the artist's albums.
    then, it will prune each of those albums down and return an iterable of those albums.
    """
    response = spot.artist_albums(url, limit=50, country="US")
    albums = response["items"]
    offset = 0
    while response["next"]: # while there is a next page, request it, then add the new albums from that new page.
        offset += 50
        response = spot.artist_albums(url, limit=50, offset=offset, country="US")
        albums += response["items"]
        
    return [prune_album(album) for album in albums] # [{}, {}, {}]
    
    
# # take each artist URL and make a pruned version of all of the albums for each.
# all_pruned_albums = (album for url in URLS for album in fetch_and_prune_albums(url)) # nested generator comprehension to flatten the albums to one level.
# albums_df = pd.DataFrame(all_pruned_albums)
# albums_df.to_csv("data/albums.csv") # send the albums DF to a .csv to temporarily cut down on queries during testing.


# ALBUM TRACKS ---------
def prune_track(track, album_id):
    return {
        "track_id": track["id"],
        "song_name": track["name"],
        "external_url": track["external_urls"]["spotify"],
        "duration_ms":  track["duration_ms"],
        "explicit": track["explicit"],
        "disc_number": track["track_number"],
        "type": track["type"],
        "song_uri": track["uri"],
        "album_id": album_id
    }

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
    
    
albums_df = pd.read_csv("data/albums.csv")
all_pruned_tracks = (track for id in albums_df["album_id"] for track in fetch_and_prune_tracks(id)) # nested generator comprehension to flatten the tracks to one level.
tracks_df = pd.DataFrame(all_pruned_tracks)
tracks_df.to_csv("data/tracks.csv")