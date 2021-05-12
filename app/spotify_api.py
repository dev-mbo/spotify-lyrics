import requests
import base64

class NoSongPlayingError(Exception):
    '''No song is playing currently'''
class TokenExpiredError(Exception):
    '''Token is expired'''


class SpotifyAPI:
    """
    Authorize at Spotify API and get current playing song 
    """

    authorize_url = "https://accounts.spotify.com/authorize"
    api_token_url = "https://accounts.spotify.com/api/token"

    current_playing_url = "https://api.spotify.com/v1/me/player/currently-playing"

    def __init__(self, client_id, client_secret, scopes, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes
        self.redirect_uri = redirect_uri
        self.access_token = ""
        self.refresh_token = ""


    def authorize(self):
        query_parameters = "?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scopes}".format(
                client_id=self.client_id, 
                redirect_uri=self.redirect_uri,
                scopes=self.scopes
            )

        url = self.authorize_url + query_parameters
        res = requests.get(url)

        return res

    
    def get_bearer_token(self):
        bearer = bytes('{}:{}'.format(self.client_id, self.client_secret), 'utf-8')
        return base64.b64encode(bearer).decode('utf-8')


    def get_access_token(self, code):
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        res = requests.post(self.api_token_url, data=data, headers={'Authorization': 'Basic ' + self.get_bearer_token()})
        
        if res.status_code != 200:
            raise Exception("http error ",res.status_code)

        json = res.json()
        self.access_token = json['access_token']
        self.refresh_token = json['refresh_token']

        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token 
        }


    def refresh_access_token(self):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }

        res = requests.post(self.api_token_url, data=data, headers={'Authorization': 'Basic ' + self.get_bearer_token() })

        if res.status_code != 200:
            raise Exception("http error: ", res.status_code)

        json = res.json()
        self.access_token = json['access_token']

        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }


    def get_currently_playing_song(self):
        res = requests.get(self.current_playing_url, headers={ 'Authorization': 'Bearer ' + self.access_token })

        if res.status_code == 401:
            raise TokenExpiredError("token is expired")
        if res.status_code == 204:
            raise NoSongPlayingError("no song is playing currently")

        if res.status_code != 200:
            raise Exception("http error: ", res.status_code)

        return res.json()