from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Create a Flask Instance
app = Flask(__name__)
# Add Datbase
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# new mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/users1'
# secret key
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"

#initialize database
db = SQLAlchemy(app)

# Create a model
class Users(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(200),nullable=False)
	email = db.Column(db.String(120),nullable=False, unique=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	#Create a string
	def __repr__(self):
		return '<Name % r>' % self.name

# Create a form class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	submit = SubmitField("Submit")



# Create a Form Class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name?", validators=[DataRequired()])
	submit = SubmitField("Submit")


@app.route('/user/add',methods=['GET','POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email= form.email.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ""
		form.email.data = ""
		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)

# Create a route decorator
@app.route('/')
def index():
	first_name = "Doug"
	favorite_pizza = ["pepporoni","Cheese",42]
	return render_template("index.html", first_name=first_name,favorite_pizza=favorite_pizza)


@app.route('/user/<name>')
def user(name):
	return render_template("user.html",user_name=name)

# Create custom error pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404

# Internal server error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"),400


# Create name page
@app.route('/name', methods=['GET','POST'])
def name():
	name = None
	form = NamerForm()
	# Validate Form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ""
		flash("Form Submitted Successfully!")

	return render_template("name.html",
		name = name,
		form = form)