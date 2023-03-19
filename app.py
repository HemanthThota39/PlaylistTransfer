from flask import Flask, redirect, request, session, url_for, render_template
import requests
from urllib.parse import urlencode
import scrap
import json

app = Flask(__name__)
app.secret_key = 'spotify_playlist_transfer'

# Set up the Spotify API credentials
client_id = 'a0800bb429564cfebffb8dda3709814f'
client_secret = '5e99af487cba46de8360b1729d1c8e34'
redirect_uri = 'http://localhost:8000/callback'

# Define the Spotify scopes required to read the user's playlist
scopes = ['playlist-read-private', 'playlist-read-collaborative', 'playlist-modify-private','playlist-modify-public']

@app.route('/')
def index():
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

@app.route('/callback')
def callback():
    # Exchange the authorization code for an access token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {client_id}:{client_secret}'
    }
    redirect_uri = 'http://localhost:8000/callback'
    data = {
        'grant_type': 'authorization_code',
        'code': str(request.args.get('code')),
        'redirect_uri': redirect_uri,
        'client_id' : 'a0800bb429564cfebffb8dda3709814f',
        'client_secret' : '5e99af487cba46de8360b1729d1c8e34',
    }
    response = requests.post(url='https://accounts.spotify.com/api/token', data=data)
    print(response.json())
    if response.status_code == 200:
        access_token = response.json()['access_token']
        session['access_token'] = access_token # store the token in the session
        return redirect(url_for('amazon'))
    else:
        return 'Failed to obtain access token'

@app.route('/amazon')
def amazon():
   return render_template('index.html')
    
@app.route('/transfer', methods=['POST'])
def transfer():
    if 'access_token' in session:
        # obtain the names of user's playlists
        url = f"https://api.spotify.com/v1/me/playlists"
        playlist_name = request.form['playlist_name']
        amazon_url = request.form['amazon_url']
        headers = {
            'Authorization': f'Bearer {session["access_token"]}', # use the token from the session
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers) # use GET instead of POST
        print(response.json())

        return str(response.json())
    else:
        return 'Please login to your Spotify account'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
