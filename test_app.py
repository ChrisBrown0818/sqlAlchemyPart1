from unittest import TestCase

from models import db, User
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test' #connects to blogly_test database, remember to create database.

app.config['SQLALCHEMY_ECHO'] = False #shows sql when running objects or app, off for testing.

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Test for opening pages/routes"""

    def setUp(self):
        """add user, executes first when running test app, runs before every method."""

        User.query.delete()
        user = User(first_name= "TestUser", last_name = "TestLastName", image_url = "TestImage")
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean up, removes all testing stuff afterwords.  Important, this runs after menthods and tests."""

        db.session.rollback() #rollback session.

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/users") #get response data of this view/route.
            html = resp.get_data(as_text=True) #response data as text.
        
        self.assertEqual(resp.status_code, 200)#assert that you get a 200 status code, or are sent succesfully to the page.
        self.assertIn('TestUser', html) #asserts that TestUser is in the response data.

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_add_user(self):
        with app.test_client() as client:
            user2 = {"first_name" : "TestUser2", "last_name" : "lastTestUser2", "image_url" : "abc" }
            resp = client.post("/users/new", data=user2, follow_redirects = True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("TestUser2", html) #important! these tests wont work, h1's on these pages show first AND last name.


    #def test_delete_user(self):
        
