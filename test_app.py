#SET UP
#import pytest
import server
import sqlite3

client = server.app.test_client()

#TEST LOGIN
def test_good_redirect():
    return
def test_bad_redirect():
    dt = client.get('/createRide')
    print(dt)
    return
def test_good_getToken():
    return
def test_bad_getToken():
    return
def test_login_create():
    return
#TEST CREATE ACCOUNT
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
def test_bad_email():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='alreadyTakenUsername',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ))
    dt = client.post('/createUser', data=dict(
        username='username',
        email='alreadyTakenUsername@example.com',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
def test_invalid_email():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='invalidEmail',
        password='passw0rd',
        password2='passw0rd'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
def test_invalid_password():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='pass',
        password2='pass'
    ), follow_redirects=True)
    assertEqual(dt.status_code, 400)
def test_no_password_match():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd2',
        password2='passw0rd'
    ))
    assertEqual(dt.status_code, 400)
def test_create_main():
    # TODO update post data dict with correct field names
    dt = client.post('/createUser', data=dict(
        username='username',
        email='joe@example.com',
        password='passw0rd',
        password2='passw0rd'
    ))
    assertEqual(dt.status_code, 200)
def test_create_login():
    #TODO client click on cancel button
    dt = client.get()
    assert 'login.css' in dt.data
def test_new_db_record():
    conn = squlite3.connect('db.squlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    assert 'username' in cur.fetchone()
#TEST INSERT RIDE
def test_bad_location():
    dt = client.post('/createRide', data=dict(
        start='your mom',
        end='gay',
        date='2018-07-22',
        time='10:00'
    ))
    assertEqual(dt.status_code, 400)
def test_locations_different():
    # TODO update post data dict with correct field names
    dt = client.post('/createRide', data=dict(
        start='10W',
        end='10W',
        date='2018-07-22',
        time='10:00'
    ))
    assertEqual(dt.status_code, 400)
def test_datefield_only_dates():
    # TODO update post data dict with correct field names
    dt = client.post('/createRide', data=dict(
        start='10W',
        end='20S',
        date='E',
        time='10:00'
    ))
    assertEqual(dt.status_code, 400)
def test_timefield_only_times():
    # TODO update post data dict with correct field names
    dt = client.post('/createRide', data=dict(
        start='10W',
        end='20S',
        date='2018-07-22',
        time='H'
    ))
    assertEqual(dt.status_code, 400)
def test_cancel_but():
    dt = client.get('/createRide')
    assert 'Cancel' in dt.data
def test_submit_but():
    dt = client.get('/createRide')
    assert 'Submit Request' in dt.data
#TEST ADD STOP
def test_start_location_invalid():
    dt = client.post('/createRide', data=dict(
        start='torg',
        end='10W',
        date='2019-07-22',
        time='14:20'
    ),follow_redirects=True)
    assertEqual(dt.status_code, 400)
def test_end_location_invalid():
    dt = client.post('/createRide', data=dict(
        start='10N',
        end='mcb',
        date='2019-07-21',
        time='10:20'
    ),follow_redirects=True)
    assertEqual(dt.status_code, 400)
def test_locations_equal():
    dt = client.post('/createRide', data=dict(
        start='10N',
        end='10N',
        date='2019-08-22',
        time='13:30'
    ),follow_redirects=True)
    assertEqual(dt.status_code, 400)
def test_add_cancel():
    dt = client.post('/createRide', data=dict(
        start='10N',
        end='50E',
        date='2017-08-19',
        time='12:00'
    ))
    assertIn(b'Cancel', dt.data)
def test_add_submit():
    dt = client.post('/createRide', data=dict(
        start='10N',
        end='50E',
        date='2017-08-19',
        time='12:00'
    ))
    assertIn(b'Submit', dt.data)
#TEST LOGOUT
def test_token_invalid():
    return
def test_logout_redirect():
    return

#TODO remove this
test_bad_redirect()