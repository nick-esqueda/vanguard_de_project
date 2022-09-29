import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from typing import Iterable
from .utils import prune_all, add_id
load_dotenv()


auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)


# ARTISTS #######################################
def fetch_artists(urls: Iterable[str]) -> list[dict]:
    """
    makes a call to the Spotify API to retrieve each artist's data from the passed in iterable. 
    returns a list of dictionaries with each artist's data. 
    """
    return spot.artists(urls)["artists"]

def extract_artists(urls: Iterable[str]) -> list[dict]:
    """
    fetches the artists' data from the Spotify API based on the passed in URLs, 
    and then prunes those JSON responses for the relevant fields.
    returns a list of those pruned objects.
    """
    print("Extracting artists...")
    artists = fetch_artists(urls)
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
        response = spot.artist_albums(url, limit=50, country="US")
        temp_albums = response["items"]
        while response["next"]: # while there is a next page, request it, then add the new albums from that new page.
            response = spot.next(response)
            temp_albums.extend(response["items"])
        
        # get and add the artist_id to each album, as it is not included in the API response.
        id = url.split('/')[-1].split('?')[0] 
        add_id(temp_albums, id, "artist_id")
        albums.extend(temp_albums)
    return albums

def extract_artists_albums(urls: Iterable[str]) -> list[dict]:
    """
    fetches all of the artists' album data from the Spotify API based on the passed in URLs, 
    and then prunes those JSON responses for the relevant fields.
    returns a list of those pruned objects.
    """
    print("Extracting albums...")
    albums = fetch_artists_albums(urls)
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
        temp_tracks = response["items"]
        while response["next"]: # while there is a next page, request it, then add the new tracks from that new page.
            response = spot.next(response)
            temp_tracks.extend(response["items"])
            
        # add the album_id to each track, as it is not included in the API response.
        add_id(temp_tracks, id, "album_id")
        tracks.extend(temp_tracks)
    return tracks
    
def extract_albums_tracks(album_ids: Iterable[str]) -> list[dict]:
    """
    fetches each album's track data from the Spotify API based on the passed in album ids, 
    and then prunes those JSON responses for the relevant fields.
    returns a list of those pruned objects.
    """
    print("Extracting tracks...")
    tracks = fetch_albums_tracks(album_ids)
    all_pruned_tracks = prune_all(tracks, "track")
    return all_pruned_tracks


# TRACK FEATURES ################################
def fetch_track_features(track_ids: list[str]) -> list[dict]:
    """
    takes in an iterable of track ids and fetches each track's "track features" from the Spotify API. 
    returns a list of those track features for each track.
    """
    offset = 0
    track_features = []
    tracks = track_ids[0:100]
    while len(tracks) > 0:
        response = spot.audio_features(tracks=tracks)
        track_features.extend(response)
        offset += 100
        tracks = track_ids[offset:offset + 100]
    return track_features

def extract_track_features(track_ids: list[str]) -> list[dict]:
    """
    fetches the tracks' "track_feature" data from the Spotify API based on the passed in track ids, 
    and then prunes those JSON responses for the relevant fields.
    returns a list of those pruned objects.
    """
    print("Extracting track features...")
    track_features = fetch_track_features(track_ids)
    pruned_track_features = prune_all(track_features, "track_features")
    return pruned_track_features
