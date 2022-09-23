import spotipy
import pandas as pd
import json
from typing import Collection, Iterable
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from artist_urls import URLS
load_dotenv()


# API SETUP #####################################
auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)


# REQUESTS ######################################
# ARTISTS ---------------------------------------
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

def create_artists_df(all_artists: Iterable[dict]) -> pd.DataFrame:
    """
    this function will go through pruned JSON responses and populate a dict with all the values.
    NOTE: this will be used to create a pandas DataFrame later.
    """
    artists = dict()
    for artist in all_artists:
        for key in artist:
            if key not in artists: # add the field name if not already there
                artists[key] = []
            artists[key].append(artist[key]) # add this artist's info to the list for each field
    
    return pd.DataFrame(artists)
    
    
# # take each artist URL and make a pruned version of the JSON response for each.
# pruned_artists = map(lambda url: fetch_and_prune_artist(url), URLS)
# # make the artists DataFrame.
# artists = create_artists_df(pruned_artists)
# print(artists)



# ALBUMS ----------------------------------------
def fetch_and_prune_albums(url: str) -> dict:
    """
    this function will take in 1 artist url, and fetch all of the artist's albums.
    then, it will prune each of those albums down and return an iterable of those albums.
    """
    # dont forget pages!!!!! next property, etc
    def prune(album):
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
        
    response = spot.artist_albums(url, limit=50)
    albums = response["items"]
    offset = 0
    while response["next"]: # while there is a next page, request it, and add the new albums.
        offset += 50
        response = spot.artist_albums(url, limit=50, offset=offset)
        albums += response["items"]
        
    pruned_albums = map(lambda album: prune(album), albums) # map[{}, {}, {}]
    return pruned_albums
    
    
test = fetch_and_prune_albums(URLS[0])
print(json.dumps(list(test), indent=2)) 

# pruned_albums = map(lambda url: fetch_and_prune_albums(url), URLS)