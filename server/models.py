from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

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

