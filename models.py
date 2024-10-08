"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import text


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
    
    @property 
    def full_name(self):
        """returns first and last name of user, makes things easier to read"""

        return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """This connects your app with your database, connect_db will be called in models file"""

    db.app = app
    app.app_context().push()
    db.init_app(app)
    


