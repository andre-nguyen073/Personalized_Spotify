# backend/config.py
import os
from dotenv import load_dotenv

# This line reads your .env file and loads the variables from it
load_dotenv() 

class Config:
    # This line safely gets the variable from the environment.
    # It says "Look for a variable named 'SPOTIFY_CLIENT_ID' and assign it here."
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")