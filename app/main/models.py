import requests
import urllib.request
import unicodedata
from app.main.spotify_api import (
    SpotifyAPI,
    TokenExpiredError,
    NoSongPlayingError
)
from bs4 import BeautifulSoup

class LyricsNotFound(Exception):
    '''Lyrics are not available for song'''

class LyricsExtractor:
    """
    Extract the lyrics for a song from genius.com 
    """
    def __init__(self):
        pass


    @staticmethod
    def get_lyrics(artist, title):
        artist = artist.replace(" ", "-").lower()
        title = title.replace(" ", "-").lower()

        artist = unicodedata.normalize('NFD', artist).encode('ascii', 'ignore').decode('utf-8')
        title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('utf-8')

        lyrics_url = "https://genius.com/{artist}-{title}-lyrics".format(artist=artist, title=title)

        print(lyrics_url)

        req = urllib.request.Request(lyrics_url, headers={
            'User-Agent': 'Mozilla'
        })

        res = urllib.request.urlopen(req)

        if res.getcode() != 200:
            raise LyricsNotFound(f"error fetching lyrics for {artist} - {title}")

        html = res.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        lyrics = soup.find("div", class_="lyrics").get_text()

        return lyrics

