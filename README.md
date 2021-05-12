# spotify-lyrics
Shows the lyrics of the current playing song on spotify

## Create Spotify API Client ID and Client Secret

- Go to https://developer.spotify.com/dashboard and sign in with your spotify account
- Create a new app e.g. `spotify-lyrics` and copy the client id  
- Edit settings afterwards and add "http://localhost:5000/callback" to the allowed Redirect URIs

Add the following environment variables to a `.env` file in your project folder:
```
CLIENT_ID=<your client ID>
CLIENT_SECRET=<your client secret>
SCOPES=user-read-private user-read-email user-read-playback-state
REDIRECT_URI=http://localhost:5000/callback
```

## Generate a Session Key

Create a random secret by using:
```
python -c 'import os; print(os.urandom(16))'
```
Add the value to the environment variable `FLASK_SECRET_KEY` in your `.env` file.

## Run app

First install all the python dependencies and create a virtual environment if you want:
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
Then start the app by typing: 
```
export FLASK_APP=run.py
flask run
```