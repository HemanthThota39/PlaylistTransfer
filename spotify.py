import requests
import json
from math import *
from tqdm import tqdm

def get_user_id(headers):
    url = f"https://api.spotify.com/v1/me"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_id = response.json()['id']
    else:
        return 'Failed to get user id'
    return user_id

def get_track_ids(songs, headers):
    track_ids = []
    for song in list(songs):
        # search the song name in spotify and get the top result and add the track id to list of track_ids
        url = f"https://api.spotify.com/v1/search?q={song[0]} {song[1]}&type=track"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            track_ids.append(response.json()['tracks']['items'][0]['id'])
        else:
            return 'Failed to get tracks'
    return track_ids

def get_new_playlist(user_id, headers, playlist_name = ''):
    if playlist_name == '':
        playlist_name = 'Amazon Music Playlist'
    url_create_playlist = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    data = {
        'name': playlist_name,
        'description': 'Playlist created from Amazon Music',
        'public': True
    }
    response = requests.post(url_create_playlist, headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        return response.json()['id']
    else:
        return 'Failed to create playlist'

def add_tracks(track_ids, playlist_id, headers):
    url_add_tracks = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    for x in range(ceil(len(track_ids)/100)):
        data = {
            'uris': [f"spotify:track:{track_id}" for track_id in track_ids[x*100:(x+1)*100]]
        }
        response = requests.post(url_add_tracks, headers=headers, data=json.dumps(data))
        if response.status_code is not 201:
            return f'Failed to add tracks to playlist, Reason: {response.reason}'  
    return('Successfully added tracks to playlist')

def create_playlist(songs, access_token, playlist_name = 'Amazon Playlist'):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    track_ids = get_track_ids(songs, headers)
    print(f'Number of Track IDs: {len(track_ids)}')

    # Get user's user_id
    user_id = get_user_id(headers)
    print(f'User ID: {user_id}')

    # Create a playlist 
    playlist_id = get_new_playlist(user_id, headers, playlist_name)
    print(f'Playlist ID: {playlist_id}')

    # Add tracks to the playlist using track_id from track_ids and playlist_id
    return add_tracks(track_ids, playlist_id, headers)
