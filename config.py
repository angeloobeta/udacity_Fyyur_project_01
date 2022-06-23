import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
username = os.environ.get('POSTGRES_USERNAME')
password = os.environ.get('POSTGRES_PASSWORD')
localhost = os.environ.get('POSTGRES_HOST')
port = os.environ.get('POSTGRES_PORT')
SQLALCHEMY_DATABASE_URI = f'postgresql://{username}:{password}@{localhost}:{port}/fyyur_artist_booking_site'


