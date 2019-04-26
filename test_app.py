#SET UP
import unittest
import server
import sqlite3
from setupdb import dbSetup

client = server.app.test_client()

class testAll(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        resetDB()

    # TEST LOGIN
    # "Login" button should take the user to the main page if credentials are correct
    def test_good_redirect(self):
        client.post('/createUser', data=dict(
            username='username',
            email='joe@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        dt = client.post('/login', data=dict(
            username='username',
            password='passw0rd',
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 200)

    # "Login" button should display an error if the credentials are not correct
    def test_bad_redirect(self):
        dt = client.post('/login', data=dict(
            username='username',
            password='passw0rd',
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # When a user logs in with correct credentials, they should recieve a valid token
    def test_good_getToken(self):
        dt = client.post('/createUser', data=dict(
            username='username',
            email='joe@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        assert b'username' in dt.data

    # When a user logs in with incorrect credentials, they should not recieve a token
    def test_bad_getToken(self):
        dt = client.post('/createUser', data=dict(
            username='username',
            email='XD',
            password='pass',
            confirmPassword='pass'
        ), follow_redirects=True)
        assert b'username' not in dt.data

    # assert create account button exists
    def test_login_create(self):
        resetDB()
        client = server.app.test_client()
        dt = client.get('/login', follow_redirects=True)
        assert b'Login' in dt.data

    # TEST CREATE ACCOUNT
    # User should recieve an error if trying to make an account that has an occupied username
    def test_bad_username(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createUser', data=dict(
            username='alreadyTakenUsername',
            email='joe@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        dt = client.post('/createUser', data=dict(
            username='alreadyTakenUsername',
            email='joe@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # User should recieve an error if trying to make an account that has an occupied email address
    def test_bad_email(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createUser', data=dict(
            username='alreadyTakenUsername',
            email='alreadyTakenEmail@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        dt = client.post('/createUser', data=dict(
            username='username',
            email='alreadyTakenEmail@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # User should recieve an error if trying to make an account that had an invalid email address
    def test_invalid_email(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createUser', data=dict(
            username='username',
            email='invalidEmail',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # User should recieve an error if the given password is less than 8 characters
    def test_invalid_password(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createUser', data=dict(
            username='username',
            email='joe@example.com',
            password='pass',
            confirmPassword='pass'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # User should recieve an error if the given password does not match the password confirmation field
    def test_no_password_match(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createUser', data=dict(
            username='username',
            email='joe@example.com',
            password='passw0rd2',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # User should not recieve an error if all fields are correct
    def test_create_main(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createUser', data=dict(
            username='test_create_main_username',
            email='test_create_main_username@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 200)

    # assert create account button exists
    def test_create_login(self):
        dt = client.get('/createUser', follow_redirects=True)
        assert b'Create Account' in dt.data

    # assert cancel button exists
    def test_create_cancel(self):
        dt = client.get('/createUser', follow_redirects=True)
        assert b'Cancel' in dt.data

    # The User's record should appear in the database
    def test_new_db_record(self):
        client.post('/createUser', data=dict(
            username='test_create_main_usernameasjknfa',
            email='testasdad_create_main_username@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        conn = sqlite3.connect('db.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM users')
        F = cur.fetchall()
        assert len(F) > 0

    # TEST INSERT RIDE
    # User should recieve an error if the start and destination are identical
    def test_locations_different(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createRide', data=dict(
            start='10W',
            end='10W',
            date='2018-07-22',
            time='10:00'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # The "Date" field should only allow dates to be entered
    def test_datefield_only_dates(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createRide', data=dict(
            start='10W',
            end='20S',
            date='E',
            time='10:00'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # The "Time" field should only allow times to be entered
    def test_timefield_only_times(self):
        # TODO update post data dict with correct field names
        dt = client.post('/createRide', data=dict(
            start='10W',
            end='20S',
            date='2018-07-22',
            time='H'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # assert cancel button exists
    def test_cancel_but(self):
        dt = client.get('/createRide', follow_redirects=True)
        assert b'Cancel' in dt.data

    # assert submit button exists
    def test_submit_but(self):
        dt1 = client.post('/createUser', data=dict(
            username='username',
            email='joe@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        dt = client.get('/createRide', follow_redirects=True)
        assert b'Submit Request' in dt.data

    # TEST ADD STOP
    # User should recieve an error if the start and destination are identical
    def test_locations_equal(self):
        dt = client.post('/addStop', data=dict(
            start='10N',
            end='10N',
            date='2019-08-22',
            time='13:30'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 400)

    # assert cancel button exists
    def test_add_cancel(self):
        client.post('/createUser', data=dict(
            username='username',
            email='joe@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        dt = client.post('/addStop', data=dict(
            start='10N',
            end='50E',
            date='2017-08-19',
            time='12:00'
        ))
        self.assertIn(b'Cancel', dt.data)

    # assert submit button exists
    def test_add_submit(self):
        client.post('/createUser', data=dict(
            username='test_add_submit',
            email='test_add_submit@example.com',
            password='test_add_submit',
            confirmPassword='test_add_submit'
        ), follow_redirects=True)
        dt = client.get('/addStop', data=dict(
            start='10N',
            end='50E',
            date='2017-08-19',
            time='12:00'
        ))
        self.assertIn(b'Submit', dt.data)

    # FIVE VALIDATION TEST CASES
    def test_login(self):
        dt = client.post('/createUser', data=dict(
            username='users',
            email='ihtc@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        dt = client.post('/login', data=dict(
            username='users',
            password='passw0rd',
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 200)
        self.assertIn(b'Available Rides', dt.data)
        assert b'Submit Request' not in dt.data

    # logout should appear on all pages once logged in
    def test_logout(self):
        # TODO update post data dict with correct field names
        client.post('/createUser', data=dict(
            username='username',
            email='joe@example.com',
            password='passw0rd',
            confirmPassword='passw0rd'
        ), follow_redirects=True)
        dt = client.get('/mainPage', follow_redirects=True)
        self.assertIn(b'Log Out', dt.data)
        dt = client.get('/addStop', follow_redirects=True)
        self.assertIn(b'Log Out', dt.data)
        dt = client.get('/createRide', follow_redirects=True)
        self.assertIn(b'Log Out', dt.data)
        dt = client.get('/riderWaiting', follow_redirects=True)
        self.assertIn(b'Log Out', dt.data)

    def test_createAcc(self):
        dt = client.post('/createUser', data=dict(
            username='test_createAccUsername',
            email='testCreateAccUsername@example.com',
            password='testCreateAcc',
            confirmPassword='testCreateAcc'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 200)
        self.assertIn(b'Available Rides', dt.data)

    def test_addRoute(self):
        client.post('/createUser', data=dict(
            username='test_addRoute',
            email='test_addRoute@example.com',
            password='test_addRoute',
            confirmPassword='test_addRoute'
        ))
        dt = client.post('/createRide', data=dict(
            start='10N',
            end='50E',
            date='2017-08-19',
            time='12:00'
        ), follow_redirects=True)
        self.assertEqual(dt.status_code, 200)
        self.assertIn(b'Available Rides', dt.data)

    def test_addStop(self):
        client.post('/createUser', data=dict(
            username='test_addStop',
            email='test_addStop@example.com',
            password='test_addStop',
            confirmPassword='test_addStop'
        ))
        client.set_cookie('localhost', 'routeid', 'test_addStop5')
        dt = client.post('/addStop', data=dict(
            username='test_createAccUsername',
            routeid='test_createAccUsername',
            start='10N',
            end='50E'
        ))
        self.assertIn(b'riderWaiting', dt.data)

def resetDB():
    dbSetup()
    conn = sqlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE users')
    cur.execute('DROP TABLE routes')
    cur.execute('DROP TABLE stops')
    conn.commit()
    conn.close()
    dbSetup()

unittest.main()
