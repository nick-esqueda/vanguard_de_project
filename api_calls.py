import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from artist_urls import URLS
from dotenv import load_dotenv
load_dotenv()

# API SETUP #####################################
auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)


# REQUESTS ######################################
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


# take each artist URL and make a pruned version of the JSON response for each.
pruned_artists = map(lambda url: fetch_and_prune_artist(url), URLS)

# go through those pruned JSON responses and populate a dict with all the values.
# NOTE: this will be used to create a pandas DataFrame later.
artists = dict()
for artist in pruned_artists:
    for key in artist:
        if key not in artists: # add the field name if not already there
            artists[key] = []
        artists[key].append(artist[key]) # add this artist's info to the list for each field
        
print(json.dumps(artists, indent=2))
