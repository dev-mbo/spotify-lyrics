from app.main.models import NoSongPlayingError, TokenExpiredError
from flask import (
    Blueprint,
    session,
    g,
    redirect,
    request,
    render_template,
    url_for
)
from app.main.models import LyricsAPI

main = Blueprint('main', __name__)

@main.route("/")
def home():
    if 'access_token' in session:
        try:
            currently_playing = g.sp.get_currently_playing_song()
            lyrics = LyricsAPI.get_lyrics_for_current_playing_song(currently_playing)
            return render_template('index.html', currently_playing=currently_playing, lyrics=lyrics)
        except KeyError as err:
            return render_template('error.html', error="artist or title could not be accessed")
        except NoSongPlayingError as err:
            return render_template('error.html', error=err)
        except TokenExpiredError as err:
            ret = g.sp.refresh_access_token()
            if 'access_token' in ret:
                session['access_token'] = ret['access_token']
            return redirect(url_for("main.home"), 302)
    else:
        res = g.sp.authorize()
        return redirect(res.url, 302)


@main.route("/callback")
def callback():
    code  = request.args.get('code')

    try:
        ret = g.sp.get_access_token(code)
        if 'access_token' in ret:
            session['access_token'] = ret['access_token']
            session['refresh_token'] = ret['refresh_token']
            return redirect(url_for("main.home"), 302)
    except Exception as err:
        return render_template('error.html', error=err)