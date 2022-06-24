from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import config
import app

moment = Moment(app)
db = SQLAlchemy(app)
app.config.from_object('config')

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['DEBUG'] = config.DEBUG
migration = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(200))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text)
    show = db.relationship('Shows', backref='venue', lazy=True)

    def __int__(self, id, name, city, state, address, phone, image_link, facebook_link,
                website, seeking_talent, seeking_description):
        self.id = id
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description


class Artist(db.Model):
    __tablename__ = 'artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.Text)
    show = db.relationship('Shows', backref='artist', lazy=True)

    def __int__(self, id, name, city, state, phone, genres, image_link, facebook_link,
                website, seeking_venue, seeking_description):
        self.id = id
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.genres = genres
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.website = website
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description



# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __int__(self, id, start_time):
        self.id = id
        self.start_time = start_time
