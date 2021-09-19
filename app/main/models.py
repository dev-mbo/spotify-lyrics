import urllib.request
import unicodedata
import re
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
        """
        Normalize the artist and title and try to retrieve the song information from genius.com
        """
        # strip feature information from title
        title = re.sub('\s*\(feat(.*?)\)', '', title)
        # replace whitespaces by dashes
        artist = artist.replace(" ", "-").lower().capitalize()
        title = title.replace(" ", "-").lower()

        # transform all unicode characters to ascii
        artist = unicodedata.normalize('NFD', artist).encode('ascii', 'ignore').decode('utf-8')
        title = unicodedata.normalize('NFD', title).encode('ascii', 'ignore').decode('utf-8')

        lyrics_url = "https://genius.com/{artist}-{title}-lyrics".format(artist=artist, title=title)

        # print("debug: " + lyrics_url)

        req = urllib.request.Request(lyrics_url, headers={
            'User-Agent': 'Mozilla'
        })

        try:
            res = urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            raise LyricsNotFound(f"Unable to find song information for {artist}-{title}: {err}")

        html = res.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        result = soup.find("div", class_="lyrics")
            
        if result:
            lyrics = result.get_text()
        else:
            raise LyricsNotFound(f"Unable to find song information for {artist}-{title}: no song information in HTML source")

        return lyrics

