#the point where all the routes are sent to the frontend
from flask import Blueprint, redirect, request, jsonify, session
from ..services import spotify_services

# A Blueprint is Flask's way of organizing groups of related routes
spotify_bp = Blueprint('spotify_bp', __name__)


# Define a route. The final URL will be `/api/spotify/profile`
@spotify_bp.route("/login") 
def spotfy_login(): 
    authorization_url = spotify_services.create_auth_url() 
    #sends you to the spofiy server
    return redirect(authorization_url)

@spotify_bp.route("/profile")
def get_profile(): 
    saved_albums = spotify_services.get_saved_albums(session["spotify_token"])
    items = saved_albums["items"] 
    names = []

    for item in items: 
        name = item["album"]['name']
        names.append(name)
    
    profile_data = {
        "token": session["spotify_token"],
        "saved_album_names": names
    }
    return jsonify(profile_data)

@spotify_bp.route("/callback") 
def get_token():  
    code = request.args.get('code') 
    error = request.args.get('error')
    if code: 
        token = spotify_services.get_tokens_from_code(code)
        #Why we can store a token in the session for the user 
        #We made a flask secret key to encrpyt the data
        session['spotify_token'] = token
        return redirect("http://127.0.0.1:5001/api/spotify/profile")
    if error: 
        print(error)
