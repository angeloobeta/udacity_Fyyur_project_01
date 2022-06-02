import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
USERNAME = os.environ.get('POSTGRES_USERNAME')
PASSWORD = os.getenv('POSTGRES_PASSWORD')
SQLALCHEMY_DATABASE_URI = f'postgresql://{USERNAME}:{PASSWORD}@localhost:5432/Fyyur_artist_booking_site'

