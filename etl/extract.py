import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from typing import Iterable, Iterator
from utils.artist_urls import ARTIST_URLS
from utils.io import send_to_csv
from utils.pruning import prune_all, add_id
load_dotenv()


auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)


# ARTISTS #######################################
def fetch_artists(urls: Iterable[str]) -> Iterator[dict]:
    """
    makes a call to the Spotify API to retrieve each artist's data from the passed in iterable. 
    returns a iterator that returns each artist's data on each iteration. 
    """
    return (spot.artist(url) for url in urls)

def extract_artists(URLS):
    artists = fetch_artists(URLS)
    pruned_artists = prune_all(artists, "artist")
    return pruned_artists


# ALBUMS ########################################
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

def extract_artists_albums(URLS):
    albums = fetch_artists_albums(URLS)
    all_pruned_albums = prune_all(albums, "album")
    return all_pruned_albums


# ALBUM TRACKS ##################################
def fetch_albums_tracks(album_ids: Iterable[str]) -> list[dict]:
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
    
def extract_albums_tracks(album_ids):
    tracks = fetch_albums_tracks(album_ids)
    all_pruned_tracks = prune_all(tracks, "track")
    return all_pruned_tracks


# TRACK FEATURES ################################
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

def extract_track_features(track_ids):
    track_features = fetch_track_features(track_ids)
    pruned_track_features = prune_all(track_features, "track_features")
    return pruned_track_features




#################################################
def main():
    artists = extract_artists(ARTIST_URLS)
    send_to_csv(artists, "data/artists.csv")
    
    albums = extract_artists_albums(ARTIST_URLS)
    send_to_csv(albums, "data/albums.csv")
    
    album_ids = (album["album_id"] for album in albums)
    tracks = extract_albums_tracks(album_ids)
    send_to_csv(tracks, "data/tracks.csv")
    
    track_ids = (track["track_id"] for track in tracks)
    track_features = extract_track_features(track_ids)
    send_to_csv(track_features, "data/track_features.csv")


if __name__ == "__main__":
    main()