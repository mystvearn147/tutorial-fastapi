import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'hello123@gmail.com', 'password': 'password123'})
    assert res.status_code == 201

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'hello123@gmail.com'


def test_login_user(client, test_user):
    res = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']})
    assert res.status_code == 200

    login_res = schemas.Token(**res.json())
    assert login_res.token_type == 'bearer'

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[
                         settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']


@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', 'password123', 403),
    ('ton@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('ton@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
