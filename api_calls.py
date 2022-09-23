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
artist_URL = "https://open.spotify.com/artist/2YZyLoL8N0Wb9xBt1NhZWg?si=Po23oXZdRRWBLqPMf70vxA"
artist = spot.artist(artist_URL)

albums = spot.artist_albums(artist_URL)
album_ids = [album["id"] for album in albums["items"]]

print(album_ids)

