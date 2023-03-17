import requests
import json

def import_songs(playlist_id):
    access_token = "BQAmgWgWdVLGZhPuii5Cx5jJZsIuL2I9tQ--Y3319kMrffYp7WLc8wvu5qLOvBGFjHBYA3AvTf99M6bePhLf9L1L-yvtLSOsaBWt7BJVvxY0E_4K2-6_ik_CeAvNGjSJotRGpy6ZQjhMCFOZ6EIzFg-CtXTHi4qp2-A0GOXvbb9n5G8-d_ntuRxZF-QNndYFwQh_4zQNFVc_OeaN9g"
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

    # extranct the song names from the playlist and store them in a list
    song_names = []
    for track in tracks:
        song_names.append(track["track"]["name"])
    return song_names