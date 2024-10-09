"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


"""default image here"""


class User(db.Model):
    """creating user table, needs an Id, first and last name, image nullable for now"""

    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)
    image_url = db.Column(db.Text, nullable = False, default= DEFAULT_IMAGE_URL)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")





    @property 
    def full_name(self):
        """returns first and last name of user, makes things easier to read"""

        return f"{self.first_name} {self.last_name}"




class Post(db.Model):
    """creating posts table, displays id, title, content, date, and foreign key"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    @property
    def friendly_date(self):
        """return better formatted date"""
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

def connect_db(app):
    """This connects your app with your database, connect_db will be called in models file"""

    db.app = app
    app.app_context().push()
    db.init_app(app)
    


