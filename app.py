from flask import Flask, render_template, request
import requests
import base64
import random
import webbrowser
import binascii
import struct

import numpy
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

#def user_auth():
    #webbrowser.open('https://accounts.spotify.com/authorize?client_id=7b0e9b57fd3649d5bba1da4bae85f429&response_type=code&redirect_uri=http://localhost:5000/')
    #r = requests.get("https://accounts.spotify.com/authorize?client_id=7b0e9b57fd3649d5bba1da4bae85f429&response_type=code&redirect_uri=http://localhost:5000/")
    #print(r)



app = Flask(__name__)
app.debug = True


def generate_key():
    key = '7b0e9b57fd3649d5bba1da4bae85f429' + ':' + '5b8712c96aab4bb4992aa7735734447c'
    spotify_key = key.encode('utf-8')
    encoded_spotify_key = base64.b64encode(spotify_key).decode("utf-8")
    return encoded_spotify_key

def get_token(key):
    r = requests.post("https://accounts.spotify.com/api/token", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": 'Basic ' + key}, data='grant_type=client_credentials')
    data = r.json()
    token = data['access_token']
    return token

def get_colors(image_file, numcolors=5, resize=150):
    input_file = requests.get(image_file, stream=True)
    # Resize image to speed up processing
    img = Image.open(input_file.raw)
    img = img.copy()
    img.thumbnail((resize, resize))

    # Reduce to palette
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

    # Find dominant colors
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    colors = list()
    for i in range(numcolors):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index*3:palette_index*3+3]
        colors.append(tuple(dominant_color))

    for x in range(len(colors)):
        colors[x] = '#%02x%02x%02x' % (colors[x][0], colors[x][1], colors[x][2])
    return colors

def get_tracks(emoji, token):
    if emoji == "broken-heart":
        playlist = '37i9dQZF1DXbrUpGvoi3TS'
    elif emoji == "person-running":
        playlist = '2DgJ11Y3E9rOS97bgaUwLH'
    elif emoji == "partying-face":
        playlist = '5ge2YqUbZrmqd2Mve8Uezf'
    elif emoji == "automobile":
        playlist = "425DKknrkKuggmrmP0ZjiS"
    elif emoji == "heart-face":
        playlist = "4QuJ2DbcTe7R8lzqfNXz7v"
    elif emoji == "grinning-face":
        playlist = "37i9dQZF1DX3rxVfibe1L0"
    elif emoji == "crying-face":
        playlist = "44tRfteJJzAmUONSiA56bQ"
    elif emoji == "santa-claus":
        playlist = "37i9dQZF1DX0Yxoavh5qJV"
    elif emoji == "canada":
        playlist = "4AZzXY9kmPXNbBxB6LumnR"
    elif emoji == "books":
        playlist = "37i9dQZF1DX8Uebhn9wzrS"
    elif emoji == "cold-face":
        playlist = "37i9dQZF1DX0XUsuxWHRQd"

    r = requests.get("https://api.spotify.com/v1/playlists/" + playlist + "/tracks", headers={
        "Authorization": 'Bearer ' + token})
    data = r.json()
    playlist = []
    album_art = []
    order = random.sample(range(49), 10)

    for x in range(10):
        playlist.append(data['items'][order[x]])
        album_art.append(get_colors(data['items'][order[x]]["track"]["album"]["images"][1]["url"]))

    print(album_art)
    return playlist, album_art


@app.route('/begin/')
def spotify_begin_app():
    return render_template('output.jinja2')


@app.route('/results/<emoji>/')
def get_emoji_choice(emoji):
    key = generate_key()
    token = get_token(key)
    track, album_art = get_tracks(emoji, token)
    #return track[0]
    return render_template('results.jinja2', tracks=track, album_art=album_art)

@app.route('/')
def hello_world():
    return render_template('output.jinja2')


