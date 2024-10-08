"""Blogly application."""


from models import db, connect_db, User
from flask import Flask, request, redirect, render_template, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
#from sqlalchemy.sql import text





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly' #connects to blogly database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #shows sql when running objects or app.
app.config['SECRET_KEY'] = "secretKey"



#toolbar = DebugToolbarExtension(app)


connect_db(app) #connect app to db 
db.create_all() #create database

@app.route('/hello')
def hello():
    return "Hello There!" #test

@app.route('/')
def home():
    """homepage redirects to users list"""

    return redirect('/users')

@app.route('/users')
def user_list():
    users = User.query.order_by(User.first_name, User.last_name).all()

    return render_template('/users/index.html', users = users)

@app.route('/users/new', methods = ["GET"])
def new_user():
    """makes add form for users"""

    return render_template('/users/new.html')


@app.route("/users/new", methods = ["POST"])  
def add_new_user():
    """add submitted user and redirect back to user index"""
    new_user = User(first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                image_url=request.form['image_url'] or None
)   #takes persons submitted info and below, adds new user to session and committs it, adding them to list/ table

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users") 


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """show user person clicked on from list"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/show.html', user = user) #user will be anchor tags and clicking on them will send them to specific user page.

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    """show from to edit user"""
    user = User.query.get_or_404(user_id)

    return render_template('users/edit.html', user = user) #using user id to send person to edit user page

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):
    """take provided input and add user to list"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect('/users') #edit user taking input and adding it to list/table


@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """handles deleting user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users') #delete using using delete forms, a post method and requires user input




