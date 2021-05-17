import requests
import urllib.parse
from app.main.spotify_api import (
    SpotifyAPI,
    TokenExpiredError,
    NoSongPlayingError
)

class LyricsNotFound(Exception):
    '''Lyrics are not available for song'''

class LyricsAPI:
    """
    Get the lyrics for a song
    """
    lyrics_url = "https://api.lyrics.ovh/v1/"

    def __init__(self):
        pass


    @staticmethod
    def get_lyrics(artist, title):
        artist = urllib.parse.quote(artist)
        title = urllib.parse.quote(title)

        res = requests.get(LyricsAPI.lyrics_url + artist + "/" + title)

        if res.status_code != 200:
            raise Exception(f"error fetching lyrics for {artist} - {title}")

        json = res.json()

        return json['lyrics']

