from flask import Flask, redirect, session, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Replace these with your actual Spotify credentials
sp_oauth = SpotifyOAuth(
    client_id='6e97c8af156649aeabb175b735db0189',
    client_secret='40cea650434a4e3394de4ab6cfd4ef25',
    redirect_uri='https://hold-music-app.onrender.com',
    scope='user-read-private user-read-email user-top-read'
)

@app.route('/')
def root():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    try:
        code = request.args.get('code')
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info

        sp = spotipy.Spotify(auth=token_info['access_token'])
        top_tracks = sp.current_user_top_tracks(time_range='short_term', limit=10)

        result = "<h2>Your Most Played Songs (last 30 days):</h2><ol>"
        for track in top_tracks['items']:
            name = track['name']
            artist = track['artists'][0]['name']
            result += f"<li>{name} by {artist}</li>"
        result += "</ol>"

        return result

    except Exception as e:
        return f"<h1>Error:</h1><pre>{str(e)}</pre>"

if __name__ == '__main__':
    print("✅ Flask is starting!")
    app.run(host='0.0.0.0', port=8080)


