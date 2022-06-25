import os
import app

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# TODO: connect to a local postgresql database
# Connect to the database
username = os.environ.get('POSTGRES_USERNAME')
password = os.environ.get('POSTGRES_PASSWORD')
localhost = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT')
SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{localhost}:{port}/fyyur_artist_booking_site'

# TODO IMPLEMENT DATABASE URL
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = DEBUG
