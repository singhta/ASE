from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flasgger import Swagger, swag_from
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,flash, redirect,url_for,session,logging,request

app = Flask(__name__)
app.debug = True
app.config['WTF_CSRF_ENABLED'] = False
CORS(app)

Swagger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

df = pd.read_csv('user.csv')


class user_cl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    #ratings = db.Column(db.Integer)
    dob = db.Column(db.String(80))
    gender  = db.Column(db.String(80))
    name = db.Column(db.String(80))

@app.route("/api/v1/get_user_details", methods=['POST', 'OPTIONS'])
def register():
    try:
        request_data =request.json
        email = request_data['email']
        password = request_data['password']
        name = request_data['name']
        username = email
        gender = request_data['gender']
        #ratings = request_data['ratings']
        dob = request_data['dob']
        #new_df = pd.DataFrame.from_dict(request_data)
        register = user_cl(username=username, name = name,password=password,gender=gender,dob=dob)
        db.session.add(register)
        db.session.commit()
        #df.append(new_df,ignore_index=True)
        return "successfully saved data"
    except Exception as e:
        return "failed to register"

@app.route("/api/v1/login", methods=['POST', 'OPTIONS'])
def login(email='',password='',test=False):

    if test == False:
        request_data = request.json
        email = request_data['email']
        password = request_data['password']
    users = user_cl.query.all()
    login = user_cl.query.filter_by(username=email, password=password).first()

    if login is not None:
        return "Login Successful"
    else:
        return "Login Failed"

def test_adduser():

    lucas=user_cl(username="lucas", email="lucas@example.com", password="test")
    user2 = user_cl(username="lucas", email="lucas@test.com")

    db.session.add(lucas)
    db.session.commit()

    assert lucas in db.session
    assert user2 not in db.session

def test_login():
    lucas=user_cl(username="lucas", email="lucas@example.com", password="test")
    db.session.add(lucas)
    db.session.commit()
    rv = login('lucas@example.com', 'test',True)
    assert 'Login Successful' == rv

@app.route("/api/v1/clear_user_table", methods=['POST', 'OPTIONS'])
def clear_table():
    try:
        db.session.query(user_cl).delete()
        db.session.commit()
        return "cleared table"
    except:
        db.session.rollback()
        return "failed to clear table"

if __name__ == '__main__':
    db.create_all()
    #clear_table()
    #test_adduser()
    #test_login()
    app.run(host='0.0.0.0', port=8080)
