from flask import Flask, redirect
from flask_cors import CORS
from config import Config

def create_app():
    # This is the application factory function
    app = Flask(__name__)
    #configure the app to have a secret key!
    app.config.from_object(Config)
    #allows flask to talk to the front end.
    CORS(app) 

    # Import and register the Spotify routes blueprint
    from .routes.spotify_routes import spotify_bp
    app.register_blueprint(spotify_bp, url_prefix='/api/spotify')

    # When you create agent_routes.py, you'll register it here too

    #testing the server
    @app.route("/")
    def index():
        return redirect("http://127.0.0.1:5001/api/spotify/login")

    return app