#SET UP
import pytest
import server

@pytest.fixture
def client():
    client = server.app.test_client()
    yield client
#TEST LOGIN

#TEST CREATE ACCOUNT

#TEST INSERT RIDE

#TEST ADD STOP