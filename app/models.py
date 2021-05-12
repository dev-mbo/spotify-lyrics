import requests
import urllib.parse
from app.spotify_api import (
    SpotifyAPI,
    TokenExpiredError,
    NoSongPlayingError
)

class LyricsAPI:
    """
    Get the lyrics for a song
    """
    lyrics_url = "https://api.lyrics.ovh/v1/"

    def __init__(self):
        pass


    def get_lyrics(self, artist, title):
        artist = urllib.parse.quote(artist)
        title = urllib.parse.quote(title)

        res = requests.get(self.lyrics_url + artist + "/" + title)

        if res.status_code != 200:
            raise Exception("error fetching lyrics")

        json = res.json()

        return json['lyrics']

