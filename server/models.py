from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort ,g, jsonify
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import config
from flask.ext.cors import CORS, cross_origin
import time
import rauth

import pandas
import simplejson as json
from app import db
from app import app

import geocoder

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://websysS16GB2:websysS16GB2!!@websys3/websysS16GB2'
app.secret_key = 'secret'

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model):
    __tablename__ = "UserInfo"
    id = db.Column('user_id', db.Integer,primary_key=True)
    username = db.Column('username', db.String(45),index=True)
    password = db.Column('password' , db.String(160))
    email = db.Column('email',db.String(45))
    firstname = db.Column('firstname',db.String(45))
    lastname = db.Column('lastname',db.String(45))
    phoneNumber = db.Column('phoneNumber',db.Integer)
    registered_on = db.Column('registered_on' , db.DateTime)
    landings = db.relationship('landing', backref='User',lazy='dynamic')
 
    def __init__(self, username, password, email, firstname, lastname):
        self.username = username
        self.set_password(password)
        self.email = email
	self.firstname = firstname
	self.lastname = lastname
	#self.phoneNumber = phoneNumber
        self.registered_on = datetime.utcnow()
    
    def set_password(self, password):
	self.password = generate_password_hash(password)

    def check_password(self, password):
	return check_password_hash(self.password, password)
			
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)
 

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

@app.before_request
def before_request():
    print "before request"
    print current_user

def get_current_user():
  return current_user

class landing(db.Model):
    __tablename__ = "OrderRequest"
    OrderID = db.Column('OrderID',db.Integer , primary_key=True)
    UserInfo_username = db.Column(db.String(45), db.ForeignKey('UserInfo.username'))
    StartTime = db.Column('StartTime' , db.DateTime)
    EndTime = db.Column('EndTime' , db.DateTime)
    Budget = db.Column('Budget',db.Integer)
    Zip = db.Column('Zip',db.Integer)
    StartLocation = db.Column('StartLocation',db.String(45))
    preference = db.Column('preference', db.String(45))
    ordered_on = db.Column('ordered_on' , db.DateTime)

    def __init__(self ,startTime, endTime, budget, location, preference):
        self.StartTime = startTime
        self.EndTime = endTime
	self.StartLocation = location
        self.Budget = budget
	self.preference = preference
        self.Zip = location
        self.ordered_on = datetime.utcnow()

@app.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
 
    username  = request.form['username']
    password  = request.form['password']
    email     = request.form['email']
    firstname = request.form['firstname'] 
    lastname  = request.form['lastname']
    user = User(username, password, email, firstname, lastname)
    db.session.add(user)
    login_user(user, remember=True)
    db.session.commit()
    
    return jsonify({ 'username': user.username, 'status' : 'success' }), 201, {'Location': url_for('login', id = user.id, _external = True)}

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({'status':'failure', 'message':'Unsupported operation : GET'})

    username = request.form['username']
    password = request.form['password']

    registered_user = User.query.filter_by(username=username).first()
    if registered_user:

      if registered_user.check_password(password):
	login_user(registered_user, remember=True)
	session['userid'] = registered_user.username
	return jsonify({'status':'success'}), 201
      else:
        flash('Username or Password is invalid' , 'error')
        return jsonify({"status":"failure", "message": "invalid password"}), 201
    return jsonify({"status":"failure", "message": "invalid username"}), 201

@app.route('/plan',methods=['GET','POST'])
def landingpage():
        if request.method == 'GET':
          return jsonify({'status':'failure', 'message':'Unsupported operation : GET'})
 
	order = landing(request.form['startTime'],request.form['endTime'], request.form['budget'],request.form['location'],request.form['preference'])
	
	order.User = get_current_user()
	loc = request.form['location']
	pref = request.form['preference']
	db.session.add(order)
        db.session.commit()
	
	def defineParams(latitude, longitude):
	  params = {}
	  params["term"] = pref
    	  params["ll"] = "{},{}".format(str(latitude), str(longitude))
    	  #params["radius_filter"] = "2000"
    	  #params["sort"] = "2"
    	  params["limit"] = "1"

    	  return params

	def getData(params):
	  # setting up personal Yelp account
    	  with open("config_secret.json",'r') as json_file:
            json_data = json.load(json_file)
    	  session = rauth.OAuth1Session(
        	consumer_key = json_data["consumer_key"]
        	,consumer_secret = json_data["consumer_secret"]
        	,access_token = json_data["token"]
        	,access_token_secret = json_data["token_secret"])

    	  request = session.get("http://api.yelp.com/v2/search", params=params)
    
	  # transforming the data in JSON format
   	  data = request.json()
    	  session.close()
    	  return data

	def result():
    	  g = geocoder.google(loc)
    	  locations = [g.latlng]

    	  apiData = []
    	  for latitude, longitude in locations:
            params = defineParams(latitude, longitude)
            apiData.append(getData(params))
            time.sleep(1.0)
	  if len(apiData) > 0:
	    try:
	    	return jsonify({"status":"success", "data" : apiData[0]["businesses"]})
	    except:
		return  jsonify({"status":"failure", "data" : apiData[0]})
	  else: 
	    return jsonify({"status": "failure"})

	return result()
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=7002,debug=True)
