from typing import Iterable, Literal


def prune_all(data: list[dict], d_type: Literal["artist", "album", "track", "track_features"]) -> list[dict]:
    """
    takes in a list of JSON responses (as dictionaries) and prunes out the relevant information for each of them, 
    returning an iterator that returns the pruned data on each iteration.
    a "d_type" must be specified to prune out the correct information.
    """
    # some data might come back with None in the response, so need to filter those out.
    return [prune(record, d_type) for record in data if record is not None]
    

def prune(data: dict, d_type: Literal["artist", "album", "track", "track_features"]) -> dict:
    """
    takes in a JSON response dictionary and prunes out the relevant information, based on the passed in "d_type".
    the d_type argument must be one of these values as a string: ["artist", "album", "track", "track_features"].
    """
    if d_type == "artist":
        return {
            "artist_id": data["id"],
            "artist_name": data["name"],
            "external_url": data["external_urls"]["spotify"],
            "genre": data["genres"][0],
            "image_url": data["images"][0]["url"],
            "followers": data["followers"]["total"],
            "popularity": data["popularity"],
            "type": data["type"],
            "artist_uri": data["uri"]
        }
        
    elif d_type == "album":
        return {
            "album_id": data["id"],
            "album_name": data["name"],
            "external_url": data["external_urls"]["spotify"],
            "image_url": data["images"][0]["url"],
            "release_date": data["release_date"],
            "total_tracks": data["total_tracks"],
            "type": data["type"],
            "album_group": data["album_group"],
            "album_uri": data["uri"],
            "artist_id": data["artist_id"]
        }
        
    elif d_type == "track":
        return {
            "track_id": data["id"],
            "song_name": data["name"],
            "external_url": data["external_urls"]["spotify"],
            "duration_ms":  data["duration_ms"],
            "explicit": data["explicit"],
            "disc_number": data["track_number"],
            "type": data["type"],
            "song_uri": data["uri"],
            "album_id": data["album_id"]
        }
        
    elif d_type == "track_features":
        return {
            "track_id": data["id"],
            "danceability": data["danceability"],
            "energy": data["energy"],
            "instrumentalness": data["instrumentalness"],
            "liveness": data["liveness"],
            "loudness": data["loudness"],
            "speechiness": data["speechiness"],
            "tempo": data["tempo"],
            "type": data["type"],
            "valence": data["valence"],
            "song_uri": data["uri"],
        }
        
    else:
        raise Exception("invalid data type. valid types: ['artist', 'album', 'track', 'track_features']")
        
        
def add_id(data: Iterable[dict], id: str, id_type: Literal["artist_id", "album_id"]) -> None:
    """
    mutates each of the given records, adding a property to it with the "id_type" as the key and "id" as the value.
    """
    for record in data:
        record[id_type] = id