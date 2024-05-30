import unittest
from app import app, db, User, Crew
from flask import url_for


class Test_App(unittest.TestCase):
    """
    A test app unittests
    """

    def setUp(self):
        """ Creates a test client """

        # Creates a test client
        self.app = app.test_client()
        self.app.testing = True

        # Pushes an application context for the tests
        self.app_context = app.app_context()
        self.app_context.push()

        # Creates a test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        db.create_all()

        # Adds some test data to the database
        self.create_test_data()

    def tearDown(self):
        """ Drops all the created tables from the test database """
        db.session.remove()
        db.drop_all()

        # Pop the application context
        self.app_context.pop()

    def create_test_data(self):
        """ Creates and adds some test users """
        user1 = User(firstname='Rob', lastname='Sande', email='rob@gmail.com',
                     password='pswrd_123')
        user1.set_password('pswrd_123')
        user2 = User(firstname='Ted', lastname='Sande', email='ted@gmail.com',
                     password='pswrd_456')
        user2.set_password('pswrd_456')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        # Create test crews
        crew1 = Crew(name='Crew1', pickupdate='2024-06-01',
                     location='Location1')
        crew2 = Crew(name='Crew2', pickupdate='2024-06-02',
                     location='Location2')
        db.session.add(crew1)
        db.session.add(crew2)
        db.session.commit()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.app.post('/login', data=dict(email='rob@gmail.com',
                                 password='pswrd_123'))
        self.assertEqual(response.status_code, 302)

    def test_login_with_wrong_client_details(self):
        response = self.app.post('/login', data=dict(email='rob@example.com',
                                 password='invalid_pswrd_123'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect password or email!', response.data)

    def test_register_route(self):
        response = self.app.post('/register', data=dict(firstname='Ruth',
                                 lastname='Sande', email='ruth@gmail.com',
                                 password='pswrd_789',
                                 confirm_password='pswrd_789'))
        self.assertEqual(response.status_code, 302)  # Redirected

        # checks if the user has been added to the database'
        user = User.query.filter_by(email='ruth@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.firstname, 'Ruth')
        self.assertEqual(user.lastname, 'Sande')

    def test_logout_route(self):
        with self.app.session_transaction() as session:
            session['name'] = 'Rob'
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_user_route(self):
        response = self.app.get('/user/Rob')
        self.assertEqual(response.status_code, 302)

    def test_edit_user_route(self):
        user = User.query.filter_by(firstname='Rob').first()
        response = self.app.post(f'edit_user/{user.id}', data=dict(
                                 editFirstname='Rob',
                                 editLastname='Sande',
                                 editPickupdate='2024-06-01',
                                 editWastetype='Plastic',
                                 editCrew='1',
                                 editPhone='275700838991',
                                 editLocation='Location1',
                                 editSubscription='Monthly')
                                 )
        self.assertEqual(response.status_code, 302)

    def test_clients_route(self):
        with self.app.session_transaction() as session:
            session['role'] = 'admin'
        response = self.app.get('/clients')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Clients', response.data)

    def test_crews_route(self):
        with self.app.session_transaction() as session:
            session['role'] = 'admin'
        response = self.app.get('/crews')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Crews', response.data)

    def test_add_crew_route(self):
        response = self.app.post('/add_crew', data=dict(
                                 name='Crew3',
                                 pickupdate='2024-06-02',
                                 location='Location3')
                                 )
        self.assertEqual(response.status_code, 302)

    def test_edit_crew_route(self):
        crew = Crew.query.filter_by(name='Crew1').first()
        response = self.app.post(f'/edit_crew/{crew.id}', data=dict(
                                 editName='Crew1',
                                 editPickupdate='2024-07-04',
                                 editLocation='Location4')
                                 )
        self.assertEqual(response.status_code, 302)


if __name__ == '__main__':
    unittest.main()
