# Web aplikacija za vremensku prognozu

Ova aplikacija je dorada Flask radionice [Flask - Vremenska prognoza](https://github.com/nikovrdoljak/flask-prognoza-radionica). Aplikacija nudi 5-dnevnu i trenutnu vremensku prognozu. Gradove čiju prognozu želite vidjeti 
je moguće birati uz pomoć tražilice ili Google Maps-a, uz to gradovi koji su traženi uz pomoć tražilice se spremaju na listu već traženih gradova.

## Tehnologije

- **Flask**: Python web framework
- **Bootstrap**: Frontend framework
- **Jinja2**: Template engine za Python
- **OpenWeather API**: API za vremenske podatke
- **Javascript**: Frontend framework, koristi se uz pomoć Bootstrap plug-in-ova u ovom projektu
- **SQLAlchemy**: Python database library

## Dorade na aplikaciji

- Dodano je nekoliko parametara poput tlaka i smjera vjetra
- Dodana je Bootswatch tema
- Dodana je opcija biranja grada uz pomoć Google Maps-a
- Dodano je spremanje već traženih gradova preko tražilice

## Upute za korištenje

1. Postavljanje API ključa na [OpenWeather](https://openweathermap.org/)
2. Pokretanje virtualne okoline, nakon čega se preporuča reinstalirati Flask, Bootstrap i SQLAlchemy da bi dobili najnovije verzije:
    ```bash
    .\venv\Scripts\Activate.ps1
    pip install flask
    pip install bootstrap-flask
    pip install SQLAlchemy
    ```
3. Pokretanje aplikacije u debug modu i postavljanje API ključa u aplikaciji:
     ```bash
     $env:FLASK_DEBUG=1
     $env:OPEN_WEATHER_API_KEY="VAŠ_OPENWEATHER_API_KEY"
     flask run
    ```
## Napomene o korištenju

1. Da bi odabir grada uz pomoć Google Maps-a radio ispravno tražilica za Grad treba biti prazna jer aplikacija priotizira tražilicu.
2. Tražilica i Google Maps se nalaze u postavkama
