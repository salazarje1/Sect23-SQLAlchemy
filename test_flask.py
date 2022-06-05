from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class AppViewsTestCase(TestCase):
    """Testing View in app"""

    def setUp(self):
        
        User.query.delete()

        user = User(first_name="Josue", last_name="Salazar")
        db.session.add(user)
        db.session.commit()

        self.id = user.id
        self.user = user

    def tearDown(self):
        """Clean Up"""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client: 
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

    def test_user_details(self): 
        with app.test_client() as client:
            resp = client.get(f'/users/{self.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-5 mb-4">Josue Salazar</h1>', html)

    def test_add_new_user(self):
        with app.test_client() as client:
            new_user = {'first_name':'Test', 'last_name':'Test', 'image_url':'img pic'}
            resp = client.post('/users/new', data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-5 mb-4">Test Test</h1>', html)

    def test_edit_user(self):
        with app.test_client() as client: 
            new_user = {'first_name':'Josh', 'last_name':'Test', 'image_url':'img pic'}
            resp = client.post(f'/users/{self.id}/edit', data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="mt-5 mb-4">Josh Test</h1>', html)