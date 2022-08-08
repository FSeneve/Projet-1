#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from models import db, Venue, Artist, Show
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
db.init_app(app)
moment = Moment(app)
app.config.from_object('config')
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  
  data = db.session.query(Venue).group_by(Venue.state, Venue.id).all()
  #num_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/venues.html', venues=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  search_term = request.form['search_term']
  search_response = db.session.query(Venue).filter(Venue.name.ilike("%" + search_term + "%")).all()
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  return render_template('pages/search_venues.html', results=search_response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  past_shows = db.session.query(Show).join(Venue, Venue.id == Show.venue_id).filter(Show.start_time < datetime.now()).filter(Venue.id == venue_id)
  past_shows_count = db.session.query(Show).join(Venue, Venue.id == Show.venue_id).filter(Show.start_time < datetime.now()).filter(Venue.id == venue_id).count()
  past_shows_list = []
  
  for p in past_shows:
    past_show = {'artist_id':p.artist_id, 'artist_name':p.artist_name, 'start_time':p.start_time, 'artist_image_link':p.artist_image_link}
    past_shows_list.append(past_show)
  
  
  upcoming_shows = db.session.query(Show).join(Venue, Venue.id == Show.venue_id).filter(Show.start_time > datetime.now()).filter(Venue.id == venue_id)
  upcoming_shows_count = db.session.query(Show).join(Venue, Venue.id == Show.venue_id).filter(Show.start_time > datetime.now()).filter(Venue.id == venue_id).count()
  upcoming_shows_list = []
  for u in upcoming_shows:
    us = {'artist_id':u.artist_id, 'artist_name':u.artist_name, 'start_time':u.start_time, 'artist_image_link':u.artist_image_link}
    upcoming_shows_list.append(us)
  
  try:
    results = db.session.query(Venue).filter(Venue.id == venue_id).all()
    myList = []
    for r in results:
      if r.upcoming_shows == None and r.past_shows == None:
        r.upcoming_shows = 'No upcoming show'
        r.past_shows = 'No past show'
      
      venue = {'id':r.id, 'name':r.name, 'city':r.city, 'state':r.state, 'genres':r.genres, 'website':r.website, 'facebook_link':r.facebook_link, 'seeking_talent':r.seeking_talent,'seeking_description':r.seeking_description,'upcoming_shows':upcoming_shows_list,'past_shows':past_shows_list, 'upcoming_shows_count':upcoming_shows_count,'past_shows_count':past_shows_count,'phone':r.phone,'address':r.address}
      myList.append(venue)
    
    
    # TODO: replace with real venue data from the venues table, using venue_id
 
    data = list(filter(lambda d: d['id'] == venue_id, myList))[0]
    return render_template('pages/show_venue.html', venue=data)
  except IndexError:
    return 'This venue doesn\'t exist!'

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
    form = VenueForm()
    if form.validate():
        try:
          venue = Venue(
          name=form.name.data,
          city=form.city.data,
          state=form.state.data, 
          address=form.address.data, 
          phone=form.phone.data,
          genres=form.genres.data, 
          facebook_link=form.facebook_link.data, 
          image_link=form.image_link.data, 
          seeking_talent=form.seeking_talent.data, 
          seeking_description=form.seeking_description.data
        )

          db.session.add(venue)
          db.session.commit()
          flash('Venue ' + request.form['name'] + ' was successfully listed!')
        except:
           # TODO: on unsuccessful db insert, flash an error instead.
         db.session.rollback()
         flash('An error occurred. Venue ' + ' could not be listed.')
         print(sys.exc_info())

        finally:
         db.session.close()
    else:
      for field, message in form.errors.items():
        flash(field + ' - ' + str(message))

    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue could not be deleted.')
  finally:
    db.session.close()
    return jsonify({'success': True})
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  search_key = request.form['search_term']
  search_response = db.session.query(Artist).filter(Artist.name.ilike("%" + search_key + "%")).all()
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
 
  return render_template('pages/search_artists.html', results=search_response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  past_shows = db.session.query(Show).join(Artist, Artist.id == Show.artist_id).filter(Show.start_time < datetime.now()).filter(Artist.id == artist_id)
  past_shows_count = db.session.query(Show).join(Artist, Artist.id == Show.artist_id).filter(Show.start_time < datetime.now()).filter(Artist.id == artist_id).count()
  past_shows_list = []
  all_artist_shows = db.session.query(Show).join(Artist, Artist.id == Show.artist_id).filter(Artist.id == artist_id)
  availability = False
  for a in all_artist_shows:
    now_time = datetime.now()
    if now_time > a.end_time:
        availability = True
        a.availability = availability
    else:
        availability = False
        a.availability = availability

  for p in past_shows:
    ps = {'artist_id':p.artist_id, 'artist_name':p.artist_name, 'start_time':p.start_time, 'artist_image_link':p.artist_image_link, 'venue_name':p.venue_name}
    past_shows_list.append(ps)
  
  
  upcoming_shows = db.session.query(Show).join(Artist, Artist.id == Show.artist_id).filter(Show.start_time > datetime.now()).filter(Artist.id == artist_id)
  upcoming_shows_count = db.session.query(Show).join(Artist, Artist.id == Show.artist_id).filter(Show.start_time > datetime.now()).filter(Artist.id == artist_id).count()
  upcoming_shows_list = []
  for u in upcoming_shows:
    us = {'artist_id':u.artist_id, 'artist_name':u.artist_name, 'start_time':u.start_time, 'artist_image_link':u.artist_image_link, 'venue_name':u.venue_name}
    upcoming_shows_list.append(us)
  
  try:
    results = db.session.query(Artist).filter(Artist.id == artist_id).all()
    myList = []
    for r in results:
      artist = {'id':r.id, 'name':r.name,'city':r.city, 'state':r.state, 'phone':r.phone, 'website':r.website, 'genres':r.genres, 'seeking_talent': r.seeking_talent, 'seeking_description':r.seeking_description, 'facebook_link':r.facebook_link, 'upcoming_shows':upcoming_shows_list, 'upcoming_shows_count':upcoming_shows_count, 'past_shows':past_shows_list, 'past_shows_count':past_shows_count, 'availability':availability}
      myList.append(artist)
    # TODO: replace with real artist data from the artists table, using artist_id
  
    data = list(filter(lambda d: d['id'] == artist_id, myList))[0]
    return render_template('pages/show_artist.html', artist=data)
  except IndexError:
    return 'This artist doesn\'t exist!' 

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist=Artist.query.get(artist_id)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  if form.validate():
    try:
      artist= Artist.query.get(artist_id)
      artist.name= form.name.data
      artist.city= form.city.data
      artist.state= form.state.data
      artist.phone= form.phone.data
      artist.genres= form.genres.data
      artist.facebook_link= form.facebook_link.data
      artist.image_link= form.image_link.data
      artist.website= form.website.data
      artist.seeking_venue= form.seeking_venue.data
      artist.seeking_description= form.seeking_description.data
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
      return redirect(url_for('show_artist', artist_id=artist_id))
    except:
      db.session.rollback()
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
      for field, message in form.errors.items():
        flash(field + ' - ' + str(message))
  return redirect(url_for('show_artist', artist_id=artist_id))
  

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form)
  venue= Venue.query.get(venue_id)
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  if form.validate():
    try: 
      venue= Venue.query.get(venue_id)
      venue.name= form.name.data
      venue.city= form.city.data
      venue.state= form.state.data
      venue.phone= form.phone.data
      venue.genres= form.genres.data
      venue.facebook_link= form.facebook_link.data
      venue.image_link= form.image_link.data
      venue.website_link= form.website_link.data
      venue.seeking_talent= form.seeking_talent.data
      venue.seeking_description= form.seeking_description.data
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
      return redirect(url_for('show_venue', venue_id=venue_id))
    except:
      db.session.rollback()
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
      print(sys.exc_info())
    finally:
      db.session.close()
  else:
    for field, message in form.errors.items():
      flash(field + ' - ' + str(message))
  return redirect(url_for('show_venue', venue_id=venue_id))
  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()
  if form.validate():
    try: 
      new_artist = Artist(
        name= form.name.data, 
        city= form.city.data, 
        state= form.state.data, 
        phone= form.phone.data, 
        website= form.website.data,
        genres= form.genres.data, 
        image_link= form.image_link.data, 
        facebook_link= form.facebook_link.data, 
        seeking_talent= form.seeking_talent.data, 
        seeking_description= form.seeking_description.data)

      db.session.add(new_artist)
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      db.session.rollback()
      flash('An error occured. '+ request.form['name'] + ' could not be listed.')
    finally:
      db.session.close()
  else:
    for field, message in form.errors.items():
      flash(field + ' - ' + str(message))
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data = db.session.query(Show).all()
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/search', methods=['POST'])
def search_shows():
  # TODO: implement search on shows with partial string search. Ensure it is case-insensitive.
  search_key = request.form['search_term']
  search_response = db.session.query(Show).join(Artist, Show.artist_id == Artist.id).filter(Artist.name.ilike("%" + search_key + "%")).all()
 
 
  return render_template('pages/show.html', results=search_response, search_term=request.form.get('search_term', ''))

@app.route('/shows/create', methods=['GET'])
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  data = Show()
  try:
    if request.method == 'POST':
      req = request.form
      venue_id = req['venue_id']
      artist_id = req['artist_id']
      artist = db.session.query(Artist).filter(Artist.id == artist_id) 
      start_time = req['start_time']
      end_time = req['end_time']
      data.venue_id = venue_id
      data.artist_id = artist_id
      for art in artist:
        data.artist_name = art.name
      
      venue = db.session.query(Venue).filter(Venue.id == venue_id)
      for ven in venue:
        data.venue_name = ven.name
      
      data.start_time = start_time
      data.end_time = end_time
      db.session.add(data)
      db.session.commit()
      flash('Show was successfully listed!')
      return redirect(request.url)
    #return render_template('forms/new_show.html')
  except:
    db.session.rollback()
    flash('A problem occured! the data didn\'t insert successfully')
  finally:
    db.session.close()


  # TODO: insert form data as a new Show record in the db, instead
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''