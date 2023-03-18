import requests
import json



def auth():
    # get the client_id and client_secret from the Spotify API
    client_id = "a0800bb429564cfebffb8dda3709814f"
    client_secret = '05b2d3c6551d4563bddecdbb5142c75c'
    # get the access token from the Spotify API
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
    }
    response = requests.post(url, data=data, headers={
        "Authorization": f"Basic {client_id}:{client_secret}",
        "Content-type": "application/x-www-form-urlencoded"
    })
    if response.ok:
        access_token = response.json()["access_token"]
        print(access_token)
    else:
        print(response.status_code, response.reason)
        return response.status_code
    
    return access_token

def import_songs(playlist_id):
    access_token = auth()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # make GET request to retrieve tracks from playlist
    playlist_id = "6uWdWOEIQxBtR12ym1ImHn"
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response = requests.get(url, headers=headers)

    # print track information
    if response.ok:
        tracks = response.json()["items"]
        for track in tracks:
            print(track["track"]["name"])
    else:
        print(response.status_code, response.reason)
        return response.status_code

    # extranct the song names from the playlist and store them in a list
    song_names = []
    for track in tracks:
        song_names.append(track["track"]["name"])
    return song_names




# def create_playlist(user_id, songs):
#     tracks_id = []
#     url_search = f"https://api.spotify.com/v1/search?q={song}&type=track"

#     # Set the Authorization header with the access token
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }
#     for song in songs:
#         #search using spotify api
#          search_params = {
#             'q': song,
#             'type': 'track'
#         }

if __name__ == '__main__':
    import_songs("6uWdWOEIQxBtR12ym1ImHn")
    
        
    

