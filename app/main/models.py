import requests
import urllib.parse
from app.main.spotify_api import (
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
    
    @staticmethod
    def get_lyrics_for_current_playing_song(current_playing):
        """
        get the lyrics for the current playing song on spotify
        current_playing: the json response for the current playing song
        """
        try:
            artist = current_playing['item']['artists'][0]['name']
            title = current_playing['item']['name']
            return LyricsAPI.get_lyrics(artist, title)
        except KeyError as err:
            raise KeyError(err)
        except Exception as err:
            raise Exception(err)

    @staticmethod
    def get_lyrics(artist, title):
        artist = urllib.parse.quote(artist)
        title = urllib.parse.quote(title)

        res = requests.get(LyricsAPI.lyrics_url + artist + "/" + title)

        if res.status_code != 200:
            raise Exception("error fetching lyrics")

        json = res.json()

        return json['lyrics']

