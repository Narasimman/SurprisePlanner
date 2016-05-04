from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, session, request, flash, url_for, redirect, render_template, abort ,g, jsonify
from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import config

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://websysS16GB2:websysS16GB2!!@websys3/websysS16GB2'
app.secret_key = 'secret'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

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
 
class landing(db.Model):
    __tablename__ = "OrderRequest"
    OrderID = db.Column('OrderID',db.Integer , primary_key=True)
    UserInfo_username = db.Column(db.String(45), db.ForeignKey('UserInfo.username'))
    StartTime = db.Column('StartTime' , db.DateTime)
    EndTime = db.Column('EndTime' , db.DateTime)
    Budget = db.Column('Budget',db.Integer)
    Zip = db.Column('Zip',db.Integer)
    ordered_on = db.Column('ordered_on' , db.DateTime)

    def __init__(self , OrderID, Budget):
        self.OrderID = OrderID
        #self.StartTime = StartTime
        #self.EndTime = EndTime
        self.Budget = Budget
        #self.Zip = Zip
        self.ordered_on = datetime.utcnow()

@app.route('/register' , methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
 
    username  = request.form['username']
    password  = request.form['password']
    email     = request.form['email']
    #firstname = request.form['firstname'] 
    #lastname  = request.form['lastname']
    firstname = ""
    lastname = ""
    user = User(username, password, email, firstname, lastname)
    db.session.add(user)
    db.session.commit()
    
    flash('User successfully registered')
    return redirect(url_for('login'))
    #return jsonify({ 'username': user.username }), 201, {'Location': url_for('login', id = user.id, _external = True)}

@app.route('/login',methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    registered_user = User.query.filter_by(username=username).first()
    flash(registered_user.check_password(password))

    if registered_user.check_password(password):
	login_user(registered_user)
	flash('Logged in successfully')
	return redirect(url_for('landingpage'))
	#return ('{"%s":"success"}'%username)
    else:
        flash('Username or Password is invalid' , 'error')
        return ('{"%s":"failure"}'%username)
        #return redirect(url_for('login'))

@app.route('/landingpage',methods=['GET','POST'])
def landingpage():
        if request.method == 'GET':
                return render_template('landingpage.html') 
	order = landing(request.form['OrderID'],request.form['Budget'])
	order.User = g.user
        db.session.add(order)
        db.session.commit()
        flash('order successfully added')
        return ('{%s,success}')
		
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002,debug=True)
