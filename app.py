from flask import Flask, redirect, request, session, url_for, render_template, jsonify
import requests
from urllib.parse import urlencode
import scrap
import json
import spotify
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
app.secret_key = 'spotify_playlist_transfer'

# Read the Spotify API credentials from environment variables
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

# Define the redirect URI for the application, be sure to add this in the Spotify developer dashboard
redirect_uri = os.environ['REDIRECT_URI']

# Define the Spotify scopes required to read the user's playlist
scopes = ['user-read-private', 'playlist-modify-private','playlist-modify-public']

# Define a global variable to store whether the user is logged in or not
logged_in = False
spotify_logo = '/static/images/spotify-logo.png'

@app.route('/')
def index():
    if(logged_in):
        display_image = spotify.get_user_image(session['access_token'])
    else:
        display_image = spotify_logo
    return render_template('index.html', logged_in=('Log out' if logged_in else 'Log in'), user_image=display_image)

@app.route('/login')
def login_oauth():
    # Construct the Spotify authorization URL
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes),
        'show_dialog': True
    }
    url = 'https://accounts.spotify.com/authorize?' + urlencode(params)
    
    # Redirect the user to the authorization URL to enter their credentials
    return redirect(url)

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    session.pop('access_token', None)
    return redirect(url_for('index'))

@app.route('/callback')
def callback():
    # Exchange the authorization code for an access token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {client_id}:{client_secret}'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': str(request.args.get('code')),
        'redirect_uri': f'{redirect_uri}',
        'client_id' : f'{client_id}',
        'client_secret' : f'{client_secret}',
    }
    response = requests.post(url='https://accounts.spotify.com/api/token', data=data)
    print(response.json())
    if response.status_code == 200:
        access_token = response.json()['access_token']
        session['access_token'] = access_token # store the token in the session
        global logged_in
        logged_in = True
        return redirect(url_for('index'))
    else:
        return 'Failed to obtain access token'

@app.route('/progress')
def progress_bar():
    fetched, total = spotify.prog()
    data = {
        'fetched' : fetched,
        'total' : total,
    }
    return json.dumps(data)

@app.route('/transfer', methods=['POST'])
def transfer():
    if 'access_token' in session:
        # Create a Spotify client object using the access token
        amazon_url = request.form['amazon_url']
        songs = scrap.getSongs(playlist_url=amazon_url)
        if songs.__len__() == 0:
            return 'Invalid Amazon Playlist URL or Empty Playlist'
        created = spotify.create_playlist(songs,session['access_token'], request.form['playlist_name'])
        if(created == 'Success'):
            return redirect(url_for('index'))
    else:
        return 'Please login to your Spotify account'

if __name__ == '__main__':
    app.run(debug=True, port=8000)