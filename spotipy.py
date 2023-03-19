import spotipy
from spotipy.oauth2 import SpotifyOAuth
import scrap

client_id = '271dd19790a44936a52d10bdb6652279' # SURAJ
client_secret = '705b4ca9de5445b38317a713990e576d'
redirect_uri = 'http://localhost:8080'
scopes = ['playlist-read-private', 'playlist-read-collaborative', 'playlist-modify-private','playlist-modify-public']

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scopes, cache_path = None, show_dialog = True, open_browser= True))

user = sp.me()
playlist_name = "Tollywood"
playlist = sp.user_playlist_create(user["id"], playlist_name, public=False)

song_titles = scrap.getSongs(playlist_url='https://music.amazon.in/user-playlists/ba16c15d870643f69891e7beaf0919f0i8n0?ref=dm_sh_6eBTNzgjrZVkdaBxwSAUp48A7')

track_uris = []
for song_title in song_titles:
    results = sp.search(q=song_title, type="track")
    if results["tracks"]["items"]:
        track_uris.append(results["tracks"]["items"][0]["uri"])

print(len(song_titles))

print(track_uris)

sp.user_playlist_add_tracks(user["id"], playlist["id"], track_uris[75:])

