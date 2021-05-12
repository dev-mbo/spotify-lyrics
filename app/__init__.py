import os
from flask import (
    Flask,
    g,
    session
)
from app.main.models import SpotifyAPI
from app.main.views import main
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET_KEY"),
        DEBUG=True,
    )

    app.register_blueprint(main)

    @app.before_request
    def get_spotify_lyrics():
        g.sp = SpotifyAPI(
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET'),
            scopes=os.getenv('SCOPES'),
            redirect_uri=os.getenv('REDIRECT_URI')
        )
        if 'access_token' in session:
            g.sp.access_token = session['access_token']

        if 'refresh_token' in session:
            g.sp.refresh_token = session['refresh_token']

    return app

