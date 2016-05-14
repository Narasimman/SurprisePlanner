from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy

from flask import Flask, session, request, flash, url_for, redirect, render_template, abort ,g, jsonify
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from flask.ext.cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
import config
import time
import rauth
import simplejson as json
import geocoder

from app import db
from app import app
from models import User, landing

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)

@app.before_request
def before_request():
    print "before request"
    print current_user

def get_current_user():
  return current_user

@app.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
 
    username  = request.form['username']
    password  = request.form['password']
    email     = request.form['email']
    firstname = request.form['firstname'] 
    lastname  = request.form['lastname']

    #validate existing user
    if User.query.filter_by(username = username).first() is not None:
        return jsonify({'status':'failure', 'message':'username already exists'}), 201

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
