## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

class AlbumEntryForm(FlaskForm):
	album_name = StringField('Enter the name of an album: ', validators=[Required()])
	rating = RadioField('How much do you like this album? (1 low, 3 high)', choices=[('1','Low'),('2','Medium'),('3', 'High')], validators=[Required()])
	submit = SubmitField('Submit')

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)



@app.route('/artistform')
def artistForm():
    return render_template('artistform.html')

@app.route('/artistinfo', methods=['POST', 'GET'])
def artistInfo():
	if request.method == 'GET':
		artist = request.args.get("artist", "")
		url = "https://itunes.apple.com/search?term=" + artist
		r = requests.get(url)
		artist_json = json.loads(r.text)

		return render_template('artist_info.html', objects=artist_json['results'])

@app.route('/artistlinks')
def artistLinks():
    return render_template('artist_links.html')

@app.route('/specific/song/<artist_name>')
def specific_artist(artist_name):
	url = "https://itunes.apple.com/search?term=" + artist_name
	r = requests.get(url)
	artist_json = json.loads(r.text)
	return render_template('specific_artist.html', results=artist_json['results'])

@app.route('/album_entry')
def album_entry():
	simpleForm = AlbumEntryForm()
	return render_template('album_entry.html', form=simpleForm)


@app.route('/album_result', methods = ['GET', 'POST'])
def album_result():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		album_name = form.album_name.data
		print(album_name)
		rating = form.rating.data
		print(rating)
		url = "https://itunes.apple.com/search?term=" + album_name + "&entity=album"
		r = requests.get(url)
		album_data = json.loads(r.text)
		album_data['search_term'] = album_name
		album_data['rating'] = rating
		print(album_data)

		return render_template('album_data.html', data=album_data)
	flash('All fields are required!')
	return redirect(url_for('album_entry'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
