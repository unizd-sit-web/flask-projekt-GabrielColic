import os
import requests
import locale
from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Optional
from flask_bootstrap import Bootstrap5
from datetime import datetime
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy

# Locale i api ključ
locale.setlocale(locale.LC_ALL, 'hr')
OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

# Inicijalizacija
app = Flask(__name__)
bootstrap = Bootstrap5(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.config['SECRET_KEY'] = 'MOJ_TAJNI_KLJUČ'
app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'cerulean'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

with app.app_context():
    db.create_all()

# Stranice

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
    units = SelectField('Mjerne jedinice', choices=[('metric', 'Metrički'), ('imperial', 'Imperijalni')], validators=[DataRequired()])
    lat = FloatField('Geografska širina', validators=[Optional()])
    lon = FloatField('Geografska dužina', validators=[Optional()])
    submit = SubmitField('Spremi')

@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        city = form.city.data.strip()
        lat = form.lat.data
        lon = form.lon.data
        
        if city:
            session['city'] = city
            session.pop('lat', None)
            session.pop('lon', None)
            existing_city = City.query.filter_by(name=city).first()
            if not existing_city:
                new_city = City(name=city)
                db.session.add(new_city)
                db.session.commit()
        elif lat and lon:
            session['lat'] = lat
            session['lon'] = lon
            session.pop('city', None)

        session['lang'] = form.lang.data
        session['units'] = form.units.data

        cache.clear()

        return redirect(url_for('settings'))

    form.city.data = session.get('city')
    form.lang.data = session.get('lang')
    form.units.data = session.get('units')
    form.lat.data = session.get('lat')
    form.lon.data = session.get('lon')

    saved_cities = City.query.all()

    return render_template('settings.html', form=form, saved_cities=saved_cities)

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

@app.route('/select_city/<city_name>')
def select_city(city_name):
    city = City.query.filter_by(name=city_name).first()
    if city:
        session['city'] = city.name
        session.pop('lat', None)
        session.pop('lon', None)
        cache.clear()
    return redirect(url_for('index'))

@app.route('/delete_cities', methods=['POST'])
def delete_cities():
    db.session.query(City).delete()
    db.session.commit()
    flash('Svi gradovi su izbrisani', 'success')
    return redirect(url_for('settings'))