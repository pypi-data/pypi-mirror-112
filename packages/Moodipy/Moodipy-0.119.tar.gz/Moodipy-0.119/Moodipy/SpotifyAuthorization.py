import requests.exceptions
import spotipy
from Moodipy.Spotipy import Spotify, User
from Moodipy.UserSummary import Person
from os import path

# Spotify Web API authorization

def Authorization():
    # Moodipy Client Environment Variables
    client_id = "17c9e6c9abe14de9bbfbb10c7d89afa4"
    client_secret = "1a8fdfd3501a4c2da9e6bd3fe300b7c8"
    redirect_uri = "http://localhost:8080"

    # User Environent Variables

    user_id = Person.userID

    scope = "user-library-read  playlist-modify-public user-top-read user-follow-read"

    # INTERFACE
    try:
        cache_name = ".cache-" + user_id
        cache_file_path = path.join(path.dirname(__file__), cache_name)
        client = Spotify(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, cache_path=cache_file_path)
        user = User(user_id=user_id, scope=scope, client=client)
        return user, client
    except (spotipy.exceptions.SpotifyException, requests.exceptions.HTTPError,spotipy.oauth2.SpotifyOauthError):
        return None

