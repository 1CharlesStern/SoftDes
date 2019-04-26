#SET UP
#import pytest
import server
import sqlite3
from setupdb import dbSetup
#TODO: Determine if database is purged between tests.  Assuming that it is for now.

client = server.app.test_client()

#TEST LOGIN
#"Login" button should take the user to the main page if credentials are correct
def test_good_redirect():
    client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    dt = client.post('/login', data=dict(
        username='username',
        password='passw0rd',
    ), follow_redirects=True)
    assertEqual(dt.status_code, 200)
#"Login" button should display an error if the credentials are not correct
def test_bad_redirect():
    dt = client.post('/login', data=dict(
        username='username',
        password='passw0rd',
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
#When a user logs in with correct credentials, they should recieve a valid token
def test_good_getToken():
    dt = client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assert 'username' in dt.data
#When a user logs in with incorrect credentials, they should not recieve a token
def test_bad_getToken():
    client.post('/createUser', data=dict(
        username='username',
        email='XD',
        password='pass',
        password2='pass'
    ), follow_redirects=True)
    assert 'username' not in dt.data
#assert create account button exists
def test_login_create():
    dt = client.get('/login', follow_redirect=True)
    assert 'Login' in dt.data
#TEST CREATE ACCOUNT
#User should recieve an error if trying to make an account that has an occupied username
def test_bad_username():
    #TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='alreadyTakenUsername',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    dt = client.post('/createUser', data=dict(
        username='alreadyTakenUsername',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if trying to make an account that has an occupied email address
def test_bad_email():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='alreadyTakenUsername',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    dt = client.post('/createUser', data=dict(
        username='username',
        email='alreadyTakenUsername@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if trying to make an account that had an invalid email address
def test_invalid_email():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='invalidEmail',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if the given password is less than 8 characters
def test_invalid_password():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='pass',
        password2='pass'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if the given password does not match the password confirmation field
def test_no_password_match():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd2',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
#User should not recieve an error if all fields are correct
def test_create_main():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 200)
#assert create account button exists
def test_create_login():
    dt = client.get('/createUser', follow_redirects=True)
    assert 'Create Account' in dt.data
#assert cancel button exists
def test_create_cancel():
    dt = client.get('/createUser', follow_redirects=True)
    assert 'Cancel' in dt.data
#The User's record should appear in the database
def test_new_db_record():
    conn = squlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    assert 'username' in cur.fetchone()
#TEST INSERT RIDE
#User should recieve an error if trying to enter an invalid start location
def test_bad_start():
    dt = client.post('/createRide', data=dict(
        start='your mom',
        end='20S',
        date='2018-07-22',
        time='10:00'
    ), follow_redirects = True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if trying to enter an invalid destination
def test_bad_end():
    dt = client.post('/createRide', data=dict(
        start='10W',
        end='gay',
        date='2018-07-22',
        time='10:00'
    ), follow_redirects = True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if the start and destination are identical
def test_locations_different():
    # TODO update post data dict with correct field names
    dt = client.post('/createRide', data=dict(
        start='10W',
        end='10W',
        date='2018-07-22',
        time='10:00'
    ), follow_redirects = True)
    assertEqual(dt.status_code, 400)
#The "Date" field should only allow dates to be entered
def test_datefield_only_dates():
    # TODO update post data dict with correct field names
    dt = client.post('/createRide', data=dict(
        start='10W',
        end='20S',
        date='E',
        time='10:00'
    ), follow_redirects = True)
    assertEqual(dt.status_code, 400)
#The "Time" field should only allow times to be entered
def test_timefield_only_times():
    # TODO update post data dict with correct field names
    dt = client.post('/createRide', data=dict(
        start='10W',
        end='20S',
        date='2018-07-22',
        time='H'
    ), follow_redirects = True)
    assertEqual(dt.status_code, 400)
#assert cancel button exists
def test_cancel_but():
    dt = client.get('/createRide', follow_redirects = True)
    assert 'Cancel' in dt.data
#assert submit button exists
def test_submit_but():
    dt = client.get('/createRide', follow_redirects = True)
    assert 'Submit Request' in dt.data
#TEST ADD STOP
#User should recieve an error if trying to enter an invalid starting location
def test_start_location_invalid():
    dt = client.post('/addStop', data=dict(
        start='torg',
        end='10W',
        date='2019-07-22',
        time='14:20'
    ),follow_redirects=True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if trying to enter an invalid destination
def test_end_location_invalid():
    dt = client.post('/addStop', data=dict(
        start='10N',
        end='mcb',
        date='2019-07-21',
        time='10:20'
    ),follow_redirects=True)
    assertEqual(dt.status_code, 400)
#User should recieve an error if the start and destination are identical
def test_locations_equal():
    dt = client.post('/addStop', data=dict(
        start='10N',
        end='10N',
        date='2019-08-22',
        time='13:30'
    ),follow_redirects=True)
    assertEqual(dt.status_code, 400)
#assert cancel button exists
def test_add_cancel():
    client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    dt = client.post('/addStop', data=dict(
        start='10N',
        end='50E',
        date='2017-08-19',
        time='12:00'
    ))
    assertIn(b'Cancel', dt.data)
#assert submit button exists
def test_add_submit():
    client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    dt = client.post('/addStop', data=dict(
        start='10N',
        end='50E',
        date='2017-08-19',
        time='12:00'
    ))
    assertIn(b'Submit', dt.data)
#TEST LOGOUT
#token should no longer be valid
def test_token_invalid():
    dt = client.get('/createRide', follow_redirect = True)
<<<<<<< Updated upstream
    assert 'Submit Request' in dt.data

#FIVE VALIDATION TEST CASES
def test_login():
    dt = client.get('/createUser', data=dict(
        username='users',
        email='ihtc@example.com',
        password='passw0rd',
        password2='passw0rd'
    ),follow_redirects=True)
    dt = client.post('/login', data=dict(
        username='users',
        password='passw0rd',
    ), follow_redirects=True)
    assertEqual(dt.status_code, 200)
    assertIn(b'Available Rides', dt.data)
=======
    assert 'Submit Request' not in dt.data
#logout should appear on all pages once logged in
>>>>>>> Stashed changes
def test_logout():
    # TODO update post data dict with correct field names
    client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    dt = client.get('/insertRoute', follow_redirect=True)
    assert 'Logout' in dt.data
    dt = client.get('/mainPage', follow_redirect=True)
    assert 'Logout' in dt.data
    dt = client.get('/addStop', follow_redirect=True)
    assert 'Logout' in dt.data
    dt = client.get('/createRide', follow_redirect=True)
    assert 'Logout' in dt.data
    dt = client.get('/riderWaiting', follow_redirect=True)
    assert 'Logout' in dt.data
def test_createAcc(): 
    dt = client.post('/createUser', data=dict(
        username='username',
        email='haha@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 200)
    assertIn(b'Available Rides', dt.data)
def test_addRoute():
    dt = client.post('/createRide', data=dict(
        start='10N',
        end='50E',
        date='2017-08-19',
        time='12:00'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 200)
    assertIn(b'Available rides', dt.data)
def test_addStop():
    dt = client.post('/addStop', data=dict(
        start='10N',
        end='50E'
    ))
    assertIn(b'Submit Request', dt.data)
    assertIn(b'Cancel', dt.data)
	
def resetDB():
	conn = squlite3.connect('db.sqlite')
    cur = conn.cursor()
    cur.execute('DROP TABLE users')
	cur.execute('DROP TABLE routes')
	cur.execute('DROP TABLE stops')
	dbSetup()