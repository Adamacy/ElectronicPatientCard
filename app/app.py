from array import array
from datetime import date
from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask.helpers import flash
from flask_pymongo import PyMongo
import json, os
from bson import json_util

app = Flask(__name__, static_folder='./static', static_url_path='')
app.config.from_object('config.DevelopmentConfig')

#mongodb+srv://Adamacy:<password>@cluster0.umzi0.mongodb.net/test

mongo = PyMongo(app)
mongo.init_app(app)

def parse_json(data):
    return json.loads(json_util.dumps(data))

@app.route('/logout')
def logoutAccount():
    session.clear()
    return render_template('public/index.html', attention='Zostałeś wylogowany')

@app.route('/')
def index():
    if 'doctor' in session:
        return render_template('public/doctor.html')
    if 'user' in session:
        pesel = session['user']['pesel']
        find = mongo.db.cards.find_one({'pesel': pesel})
        
        return render_template('public/patientcard.html', data=find)
    return render_template('public/index.html')

@app.route('/new')
def newcard():
    return render_template('public/newcard.html')

@app.route('/newinfo')
def render_informations():
    return render_template('public/newinfo.html')

@app.route('/doctorcard')
def dCard():
    return render_template('public/doctor.html')

@app.route('/render_health')
def rH():
    pesel = session['user']['pesel']
    find = mongo.db.healthStatus.find_one({'pesel': pesel})
    if find != None:
        return render_template('public/health.html', data=find)
    return render_template('public/health.html', data='Nie ma żadnych danych')

@app.route('/login', methods=['POST'])
def login_card():
    data = {
        'phone': request.form.get('phone'),
        'pesel': request.form.get('pesel'),
    }
    find = mongo.db.cards.find_one({'pesel': data['pesel']})
    
    if find == None:
        return render_template('public/index.html', attention='Nie posiadasz karty na naszej stronie, prosimy najpierw o jej utworzenie.')
    else:
        session['user'] = data
        return render_template('public/patientcard.html', data=find, time=date.today())

@app.route('/registercard', methods=['POST'])
def create():
    data = {
        'name': request.form.get('name'),
        'surname': request.form.get('surname'),
        'adress': request.form.get('adress'),
        'pesel': request.form.get('pesel'),
        'phone': request.form.get('phone'),
        'born': request.form.get('born'),
    }
    find = mongo.db.cards.find_one({'pesel': data['pesel']})
    
    if find != None:
        return 'Podano złe dane'
    mongo.db.cards.insert_one(data)
    return render_template('public/index.html', attention='Karta została utworzona')

@app.route('/visit', methods=['POST'])
def create_visit():
    pesel = session['user']['pesel']
    data = {
        'name': request.form.get('name'),
        'surname': request.form.get('surname'),
        'postalcode': request.form.get('postalcode'),
        'city': request.form.get('city'),
        'born': request.form.get('born'),
        'visit_date': request.form.get('visit'),
        'pesel': pesel
    }
    visit = data['visit_date']
    mongo.db.visits.insert_one(data)
    return f'Wizyta została umówiona na: {visit}'

@app.route('/visits')
def visits_history():
    data = session['user']
    find = mongo.db.visits.find({'pesel': data['pesel']})
    visits = []
    for x in find:
        visits.append(x)
    return render_template('public/patientcard.html', data=visits)

@app.route('/doctor', methods=['POST'])
def loginDoctor():
    doctorID = request.form.get('doctorID')
    find = mongo.db.doctors.find_one({'doctorID': doctorID})
    if find == None:
        return 'Nie isnieje konto z takim identyfikatorem, żeby takie utworzyć zgłoś się do zarządcy placówki.'
    session['doctor'] = doctorID
    return renderPage()

def renderPage():
    array = []
    find = mongo.db.cards.find({})
    for x in find:
        print(x)
        array.append(x)
    return render_template('public/doctor.html', data=array)

@app.route('/details/<pesel>', methods=['POST', 'GET'])
def find_patient(pesel):
    find = mongo.db.healthStatus.find_one({'pesel': pesel})
    if find == None:
        return render_template('public/newinfo.html', pesel=pesel)
    return render_template('public/details.html', data=find)

@app.route('/newinfo/<pesel>')
def cos(pesel):
    return render_template('public/newinfo.html', pesel=pesel)

@app.route('/create', methods=['POST'])
def createStatus():
    data = {
        'leukocyty': request.form.get('leukocyt'),
        'erytrocyty': request.form.get('erytrocyt'),
        'hemoglobina': request.form.get('hemoglobina'),
        'hematokryt': request.form.get('hematokryt'),
        'mcv': request.form.get('mcv'),
        'mch': request.form.get('mch'),
        'mchc': request.form.get('mchc'),
        'plytki': request.form.get('plytki'),
        'limfocyty': request.form.get('limfocyt'),
        'inne': request.form.get('inne'),
        'neutrofile': request.form.get('neutrofile'),
        'rdw': request.form.get('rdw'),
        'pdw': request.form.get('pdw'),
        'mpv': request.form.get('mpv'),
        'lcr': request.form.get('lcr'),
        'przejrzystosc': request.form.get('przejrzystosc'),
        'barwa': request.form.get('barwa'),
        'ciezar': request.form.get('ciezar'),
        'pH': request.form.get('pH'),
        'glukoza': request.form.get('glukoza'),
        'ketony': request.form.get('ketony'),
        'urubilinogen': request.form.get('urubilinogen'),
        'urubilinogen': request.form.get('urubilinogen'),
        'bialka': request.form.get('bialka'),
        'azotyny': request.form.get('azotyny'),
        'erytrocyty_mocz': request.form.get('erytrocyt_mocz'),
        'leukocyt_mocz': request.form.get('leukocyt_mocz'),
        'nablonki': request.form.get('nablonki'),
        'leukocyt_osad': request.form.get('leukocyt_osad'),
        'erytrocyty_swieze': request.form.get('erytrocyty_swieze'),
        'erytrocyt_wylugowny': request.form.get('erytrocyt_wylugowny'),
        'bakterie': request.form.get('bakterie'),
        'kreatynina': request.form.get('kreatynina'),
        'egfr': request.form.get('egfr'),
        'glukoza_mocz': request.form.get('glukoza_mocz'),
        'crp': request.form.get('crp'),
        'tsh': request.form.get('tsh'),
        'pesel': request.form.get('pesel')
    }
    find = mongo.db.healthStatus.find_one({'pesel': data['pesel']})
    if find != None:
        mongo.db.healthStatus.update_one(find, {'$set': data})
        return 'Dane zostały zmienione'
    else:
        mongo.db.healthStatus.insert_one(data)
    return parse_json(data)

if __name__ == '__main__':
    app.run(threaded=True, debug=True)