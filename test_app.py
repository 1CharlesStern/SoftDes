#SET UP
#import pytest
import server
import sqlite3

client = server.app.test_client()
create
#TEST LOGIN
def test_good_redirect():
    return
def test_bad_redirect():
    dt = client.get('/login')
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
    return
def test_locations_different():
    return
def test_datefield_only_dates():
    return
def test_timefield_only_times():
    return
def test_cancel_main():
    return
def test_submit_main():
    return
#TEST ADD STOP
def test_location_invalid():
    return
def test_locations_equal():
    return
def test_add_cancel():
    return
def test_add_submit():
    return
#TEST LOGOUT
def test_token_invalid():
    return
def test_logout_redirect():
    return

#TODO remove this
test_bad_redirect()