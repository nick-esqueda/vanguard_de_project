def prune(data, d_type):
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
            "album_uri": data["uri"],
            "artist_id": data["artists"][0]["id"]
        }
        
    elif d_type == "track": # OG prune_track() took in an album_id param
        return {
            "track_id": data["id"],
            "song_name": data["name"],
            "external_url": data["external_urls"]["spotify"],
            "duration_ms":  data["duration_ms"],
            "explicit": data["explicit"],
            "disc_number": data["track_number"],
            "type": data["type"],
            "song_uri": data["uri"],
            "album_id": album_id # this is a problem
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
        