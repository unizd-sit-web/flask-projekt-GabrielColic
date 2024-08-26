import os
import requests
import locale
from flask import Flask, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Optional
from flask_bootstrap import Bootstrap5
from datetime import datetime
from flask_caching import Cache

# Configure locale and API key
locale.setlocale(locale.LC_ALL, 'hr')
OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

# Initialize Flask app, Bootstrap, and Cache
app = Flask(__name__)
bootstrap = Bootstrap5(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config['SECRET_KEY'] = 'MOJ_TAJNI_KLJUČ'
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'cerulean'

@app.route('/')
@cache.cached(timeout=60)
def index():
    url = 'https://api.openweathermap.org/data/2.5/weather'
    lat = session.get('lat')
    lon = session.get('lon')
    city = session.get('city') if session.get('city') else 'zadar'
    
    parameters = {
        'appid': OPEN_WEATHER_API_KEY,
        'units': session.get('units'),
        'lang': session.get('lang')
    }
    
    if lat and lon:
        parameters['lat'] = lat
        parameters['lon'] = lon
    else:
        parameters['q'] = city

    response = requests.get(url, params=parameters)
    weather = response.json()
    print(datetime.now())
    return render_template('index.html', weather=weather, session=session, datetime=datetime)

class SettingsForm(FlaskForm):
    city = StringField('Grad')
    lang = SelectField('Jezik', choices=[('hr', 'Hrvatski'), ('en', 'English'), ('de', 'Deutsch')], validators=[DataRequired()])
    units = SelectField(choices=[('metric', 'Metric'), ('imperial', 'Imperial')], validators=[DataRequired()])
    lat = FloatField('Latitude', validators=[Optional()])
    lon = FloatField('Longitude', validators=[Optional()])
    submit = SubmitField('Spremi')

@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        city = form.city.data.strip()
        lat = form.lat.data
        lon = form.lon.data

        print(f"Submitted City: {city}, Latitude: {lat}, Longitude: {lon}")
        
        
        if city:
            session['city'] = city
            session.pop('lat', None)  # Remove latitude if city is provided
            session.pop('lon', None)  # Remove longitude if city is provided
        elif lat and lon:
            session['lat'] = lat
            session['lon'] = lon
            session.pop('city', None)  # Remove city if coordinates are provided

        session['lang'] = form.lang.data
        session['units'] = form.units.data

        print(f"Session Data After Submit: {session}")

        cache.clear()

        return redirect(url_for('settings'))

    form.city.data = session.get('city')
    form.lang.data = session.get('lang')
    form.units.data = session.get('units')
    form.lat.data = session.get('lat')
    form.lon.data = session.get('lon')

    return render_template('settings.html', form=form)

@app.template_filter('datetime')
def format_datetime(value, format='%d.%m.%Y %H:%M'):
    if format == 'time':
        format = '%H:%M'
    return datetime.fromtimestamp(value).strftime(format)

@app.route('/forecast_days')
def forecast_days():
    url = 'http://api.openweathermap.org/data/2.5/forecast'
    lat = session.get('lat')
    lon = session.get('lon')
    city = session.get('city') if session.get('city') else 'zadar'
    
    parameters = {
        'appid': OPEN_WEATHER_API_KEY,
        'units': session.get('units'),
        'lang': session.get('lang')
    }
    
    if lat and lon:
        parameters['lat'] = lat
        parameters['lon'] = lon
    else:
        parameters['q'] = city

    response = requests.get(url, params=parameters)
    weather = response.json()
    return render_template('forecast_days.html', weather=weather)