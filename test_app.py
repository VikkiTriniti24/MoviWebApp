import pytest
from app import app
from datamanager.sqlite_data_manager import SQLiteDataManager, User

@pytest.fixture
def client():
    app.config['TESTING'] = True

    app.data_manager = SQLiteDataManager()
    app.data_manager.reset_database()

    # Testdaten anlegen
    user = User(name="TestUser")
    app.data_manager.add_user(user)

    with app.test_client() as client:
        yield client

def test_homepage(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"TestUser" in rv.data

def test_add_user(client):
    rv = client.post('/add_user', data={'name': 'NewUser'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"NewUser" in rv.data

def test_user_movies(client):
    user = app.data_manager.get_all_users()[0]
    rv = client.get(f'/users/{user.id}')
    assert rv.status_code == 200
    # Überschrift enthält "Filme von TestUser"
    assert bytes(f"Filme von {user.name}", 'utf-8') in rv.data

def test_add_movie(client):
    user = app.data_manager.get_all_users()[0]
    rv = client.post(
        f'/users/{user.id}/add_movie',
        data={'title': 'New Movie', 'year': '2025'},
        follow_redirects=True
    )
    assert rv.status_code == 200
    assert b"New Movie" in rv.data


