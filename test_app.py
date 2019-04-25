#SET UP
import pytest
import server

client = server.app.test_client()
#TEST LOGIN
def test_good_redirect():
    return
def test_bad_redirect():
    return
def test_good_getToken():
    return
def test_bad_getToken():
    return
def test_login_create():
    return
#TEST CREATE ACCOUNT
def test_bad_username():
    return
def test_bad_email():
    return
def test_invalid_email():
    return
def test_invalid_password():
    return
def test_no_password_match():
    return
def test_create_main():
    return
def test_create_login():
    return
def test_new_db_record():
    return
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