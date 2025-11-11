#services gives information to routes to send to the frontend
from flask import session
import base64
from requests import post
import requests
import json
from requests import get 
from urllib.parse import urlencode
from config import Config
#This immidiately starts looking for the .dotenv file
#it even looks through the parent folders

redirect_url = 'http://127.0.0.1:5001/api/spotify/callback'

def create_auth_url():  
    #everytime we change the scope we have to reverify
    base_url = "https://accounts.spotify.com/authorize?"
    scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read user-read-email"
    params = { 
        'client_id': Config.SPOTIFY_CLIENT_ID, 
        'response_type': 'code',
        'redirect_uri': redirect_url, 
        "scope": scope
    }
    #needed to turn the params directionary into the format web url uses
    complete_url = base_url + urlencode(params) 
    return complete_url  

#when you log in spotify sends back a code, must convert that code into a token?
def get_tokens_from_code(code):   
    url = "https://accounts.spotify.com/api/token"
    auth_string = Config.SPOTIFY_CLIENT_ID+ ":" + Config.SPOTIFY_CLIENT_SECRET 
    auth_bytes = auth_string.encode("utf-8") 
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = { 
        "Authorization": "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"
    } 

    data = {
        "grant_type": "authorization_code", 
        "code": code, 
        "redirect_uri": redirect_url
        }
    
    result = post(url, headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

def get_saved_albums(token): 
    url = "https://api.spotify.com/v1/me/albums" 
    headers = {  
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    } 
    response = requests.get(url, headers=headers)
    return response.json()
