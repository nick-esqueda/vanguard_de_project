import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
from dotenv import load_dotenv
load_dotenv()

auth_manager = SpotifyClientCredentials()
spot = spotipy.Spotify(auth_manager=auth_manager)

URL = "https://open.spotify.com/artist/2YZyLoL8N0Wb9xBt1NhZWg?si=Po23oXZdRRWBLqPMf70vxA"
albums = spot.artist_albums(URL)
print(json.dumps(albums, indent=2))