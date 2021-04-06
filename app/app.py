from array import array
from datetime import date
from flask import Flask, render_template, url_for, request, session, flash
from flask.helpers import flash
from flask_pymongo import PyMongo
import json
from bson import json_util

app = Flask(__name__, static_folder='./static', static_url_path='')
app.config.from_object('config.DevelopmentConfig')

mongo = PyMongo(app)
mongo.init_app(app)

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/render_login_page')
def render_card():
    return render_template('public/logincard.html')

@app.route('/new')
def newcard():
    return render_template('public/newcard.html')

@app.route('/doctor')
def dCard():
    return render_template('public/doctor.html')

@app.route('/render_health')
def rH():
    return render_template('public/health.html')

@app.route('/login', methods=['POST'])
def login_card():
    data = {
        'phone': request.form.get('phone'),
        'pesel': request.form.get('pesel'),
    }
    find = mongo.db.cards.find_one({'pesel': data['pesel']})
    session['user'] = data
    if find == None:
        return render_template('public/logincard.html', attention='Nie posiadasz karty na naszej stronie, prosimy najpierw o jej utworzenie.')
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
    return 'Karta została utworzona'

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

@app.route('/health')
def health_checker():
    pass

@app.route('/patients')
def renderPage():
    array = []
    find = mongo.db.cards.find({})
    for x in find:
        array.append(x)
    return render_template('public/doctor.html', data=array)

@app.route('/details/<pesel>', methods=['POST', 'GET'])
def find_patient(pesel):
    find = mongo.db.healthStatus.find_one({'pesel': pesel})
    print(find)
    if find == None:
        return '''
                <h3>Nie można znaleść stanu zdrowia pacjenta!</h3>
                <form action="create" method="POST"> 
                    <input type="text" name="holestelor" placeholder="holesterol?"/>
                    <input type="submit" value="utwórz"/>
                </form>
        '''
    return render_template('public/details.html', data=find)

@app.route('/create')
def createStatus():
    data = {
        'holestelor': request.form.get('holestelor')
    }
    mongo.db.healthStatus.insert_one(data)
if __name__ == '__main__':
    app.run(debug=True)