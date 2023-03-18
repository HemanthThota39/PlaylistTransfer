from flask import Flask, Response, redirect, request, render_template
import requests
import spotify
import scrap


playlistTransfer = Flask(__name__)


@playlistTransfer.route('/')
def index():
    return render_template('index.html')


@playlistTransfer.route('/transfer', methods=['POST'])
def transfer():
    # get the form data
    amazon_url = request.form['amazon_url']
    spotify_user_id = request.form['spotify_user_id']

    # get the songs from Amazon Music
    songs = scrap.getSongs(playlist_url=amazon_url)

    # import the songs to Spotify
    # playlist_id = spotify.create_playlist(spotify_user_id, 'Amazon Music Transfer')
    # spotify.add_songs_to_playlist(playlist_id, songs)

    # return a success message
    print(songs)
    print("\n\n")
    print(len(songs))
    return "Playlist transfer complete!"


if __name__ == '__main__':
    playlistTransfer.run(debug=True)

