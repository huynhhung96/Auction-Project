from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
session = sessionmaker()
#Config PostgresSQL
app = Flask(__name__)
app.debug = True
app.config['SQLAlchemy_DATABASE_URI'] = 'postgresql://postgres:352407442@localhost/Flask_Postgres_ML'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
#Create 3 models and mappings

class Items(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30), nullable = False)
	description = db.Column(db.String(50), nullable = False)
	start_time = db.Column(db.DateTime)

	autioneer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
	bider_id = db.Column(db.Integer, db.ForeignKey('bid.bider_id'), nullable = False)
	def __init__(self, name, description, start_time):
		self.name = name
		self.description = description
		self.start_time = start_time
	def __repr__(self):
		return '<Name %r, Description %r, Start time %r>' % (self.name, self.description, self.start_time)

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True, default=lambda: uuid.uuid4().hex)
	username = db.Column(db.String(30), nullable = False)
	password = db.Column(db.String(30), nullable = False)

	bid = db.relationship('Bid', backref = 'bider', lazy = True, primaryjoin = 'Bid.bider_id == User.id')
	auc_items = db.relationship('Items', backref = 'auctioneer', lazy = True, primaryjoin = 'User.id == Items.autioneer_id')

	def __init__(self,  username, password):
		self.username = username
		self.password = password
	def __repr__(self):
		return '<User ID %r, Username %r, Password %r, Bid %r>' % (self.id, self.username, self.password, self.bid)

class Bid(db.Model):
	__tablename__ = 'bid'
	id = db.Column(db.Integer, primary_key = True)
	price = db.Column(db.Float, nullable = False)

	bider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	bided_items = db.relationship('Items', backref = 'bided', lazy = True, primaryjoin = 'Bid.bider_id == Items.bider_id')
	def __init__(self, price):
		self.price = price
	def __repr__(self):
		return '<ID %r, Price %r, Bider id %r, Bided items %r>' % (self.id, self.price, self.bider_id, self.bided_items)


#Insert demo data
item1 =Items(name ='Baseball', description ='Just a baseball', start_time = '2017-03-28')

user1 = User(username = 'Steve', password = '123')
user2 = User(username = 'Micheal', password = '456')
user3 = User(username = 'Jane', password = '789')

bid1 = Bid(price ='1000')
bid2 = Bid(price ='1500')

item1.auctioneer_id = user1.id
bid1.bider_id = user2.id
bid2.bider_id = user3.id

s = session()
s.add(item1)
s.add(user1)
s.add(user2)
s.add(user3)
s.add(bid1)

db.session.commit

max1 =s.query(func.max(Bid.price))

	print(max1)


