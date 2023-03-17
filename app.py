from flask import Flask, Response, redirect
from flask import request
from flask import render_template
import requests
import spotify


playlistTransfer = Flask(__name__)


@playlistTransfer.route('/playlists/<playlist_id>')
def playlists(playlist_id):
    # set up authorization headers
    songs_list = spotify.import_songs(playlist_id)
    return songs_list

if __name__ == '__main__':
    playlistTransfer.run(host='0.0.0.0')
