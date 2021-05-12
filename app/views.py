from app.models import NoSongPlayingError, TokenExpiredError
from app import app
from flask import (
    session,
    g,
    redirect,
    request,
    render_template
)
from app.models import LyricsAPI

@app.route("/")
def main():
    if 'access_token' in session:
        try:
            currently_playing = g.sp.get_currently_playing_song()
            artist = currently_playing['item']['artists'][0]['name']
            title = currently_playing['item']['name']
            lyrics_api = LyricsAPI()
            lyrics = lyrics_api.get_lyrics(artist, title)
            return render_template('index.html', currently_playing=currently_playing, lyrics=lyrics)
        except KeyError as err:
            return render_template('error.html', error="artist or title could not be accessed")
        except NoSongPlayingError as err:
            return render_template('error.html', error=err)
        except TokenExpiredError as err:
            ret = g.sp.refresh_access_token()
            if 'access_token' in ret:
                session['access_token'] = ret['access_token']

            return redirect("/", 302)
    else:
        res = g.sp.authorize()
        return redirect(res.url, 302)


@app.route("/callback")
def callback():
    code  = request.args.get('code')

    try:
        ret = g.sp.get_access_token(code)
        if 'access_token' in ret:
            session['access_token'] = ret['access_token']
            session['refresh_token'] = ret['refresh_token']
            return redirect("/", 302)
    except Exception as err:
        return render_template('error.html', error=err)