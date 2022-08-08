from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    website = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(500))
    past_shows = db.Column(db.String(120))
    pastShowsCount = db.Column(db.Integer)
    upcoming_shows = db.Column(db.String(120))
    upcomingShowsCount = db.Column(db.Integer)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default = False)
    seeking_description = db.Column(db.String(500))
    past_shows = db.Column(db.String(120))
    pastShowsCount = db.Column(db.Integer)
    upcoming_shows = db.Column(db.String(120))
    upcomingShowsCount = db.Column(db.Integer)
    availability = db.Column(db.Boolean, default = True)
    venues = db.relationship('Venue', backref = db.backref('artists', lazy = True))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
 
  artist_name = db.Column(db.String(20))
  venue_name = db.Column(db.String(20))
  artist_image_link = db.Column(db.String(30))
  start_time = db.Column(db.DateTime)
  end_time = db.Column(db.DateTime)
 