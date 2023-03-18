from flask import Flask, redirect, request, session, url_for, render_template
import requests
from urllib.parse import urlencode
import scrap
import json


app = Flask(__name__)

# Set up the Spotify API credentials
client_id = 'a0800bb429564cfebffb8dda3709814f'
client_secret = '5e99af487cba46de8360b1729d1c8e34'
redirect_uri = 'http://localhost:5000/callback'
app.secret_key = 'Hem998$$'
# Define the Spotify scopes required to read the user's playlist
scopes = ['playlist-read-private', 'playlist-read-collaborative', 'playlist-modify-private','playlist-modify-public']

@app.route('/login')
def login():
    # Construct the Spotify authorization URL
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes),
        'show_dialog': False

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
    print(request.args.get('code'))
    redirect_uri = 'http://localhost:5000/callback'
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
        session['access_token'] = access_token
        return redirect(url_for('index'))
    else:
        return 'Failed to obtain access token'

@app.route('/')
def index():
   return render_template('index.html')
    
@app.route('/transfer', methods=['POST'])
def transfer():
    if 'access_token' in session:
        # Create a Spotify client object using the access token
        amazon_url = request.form['amazon_url']
        songs = scrap.getSongs(playlist_url=amazon_url)
        track_ids = []
        for song in list(songs)[:5]:
            #search the song name in spotify and get the top result and add the track id to list of track_ids
            url = f"https://api.spotify.com/v1/search?q={song}&type=track"
            headers = {
                'Authorization': f'Bearer {session["access_token"]}',
                'Content-Type': 'application/json',
            }
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                track_ids.append(response.json()['tracks']['items'][0]['id'])
            else:
                return 'Failed to get tracks'
        
        print(track_ids)
        #get user's user_id
        url = f"https://api.spotify.com/v1/me"
        headers = {
            'Authorization': f'Bearer {session["access_token"]}',
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_id = response.json()['id']
        else:
            return 'Failed to get user id'
        print(user_id)

        #create a playlist 
        url_create_playlist = f"https://api.spotify.com/v1/users/{user_id}/playlists"
        headers = {
            'Authorization': f'Bearer {session["access_token"]}',
            'Content-Type': 'application/json',
        }
        data = {
            'name': 'Amazon Playlist',
            'description': 'Playlist created from Amazon Music',
            'public': True
        }
        response = requests.post(url_create_playlist, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            playlist_id = response.json()['id']
        else:
            return 'Failed to create playlist'
        print(playlist_id)

        #add tracks to the playlist using track_id from track_ids and playlist_id
        url_add_tracks = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            'Authorization': f'Bearer {session["access_token"]}',
            'Content-Type': 'application/json',
        }
        data = {
            'uris': [f"spotify:track:{track_id}" for track_id in track_ids]
        }
        response = requests.post(url_add_tracks, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            print('Successfully added tracks to playlist')
        else:
            return 'Failed to add tracks to playlist'
        

        
            
        return 'Success!'
    else:
        return 'Please login to your Spotify account'

if __name__ == '__main__':
    app.run(debug=True)
