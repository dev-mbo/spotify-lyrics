from app.models import NoSongPlayingError
from app import app
from flask import (
    session,
    g,
    redirect,
    request,
    render_template
)

@app.route("/")
def main():
    if 'access_token' in session:
        try:
            currently_playing = g.sp.get_currently_playing_song()
            return render_template('index.html', currently_playing=currently_playing)
        except NoSongPlayingError as err:
            return render_template('error.html', error=err)
        except Exception as err:
            ret = g.sp.refresh_access_token()
            return render_template('error.html', error=err)
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