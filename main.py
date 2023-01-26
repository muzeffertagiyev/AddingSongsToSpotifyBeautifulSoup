from urllib import request
import requests
from bs4 import BeautifulSoup
import pprint
import os

URL = "https://www.billboard.com/charts/hot-100"
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"))

# this for getting example url for getting user token

# results = sp.current_user_saved_tracks()
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"{URL}/{date}/")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
song_names = soup.select(".lrv-u-width-100p li h3")

user_id = sp.current_user()['id']

songs = []
song_uris = []
year = date.split("-")[0]

for song in song_names:
    song_name = song.getText()
    corrected_name = ''.join(song_name.split())
    # it make spaces between words which starts with capital letters
    name=''
    for i in range(len(corrected_name)):
        if corrected_name[i].isupper() and i != 0:
            name += " "
            name += corrected_name[i]
        else:
            name += corrected_name[i]
    songs.append(name)


for song in songs:
    result  = sp.search(q=f"track:{song} year:{year}", type='track')
    # pprint.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pprint.pprint(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f'{date} Billboard 100',public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


