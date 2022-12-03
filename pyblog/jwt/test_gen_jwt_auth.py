from requests import exceptions
from unittest.mock import patch
import gen_jwt_auth

CREDS = {
    "wp_posts_url": "http://18.189.31.189:8088/wp-json/wp/v2/posts",
    "wp_jwt_auth_url": "http://18.189.31.189:8088/wp-json/jwt-auth/v1/token",
    "user": "test_user",
    "password": "test_password",
    "jwt_auth": "test_jwt-auth"
}

def test_get_jwt_auth_success():
    expected = {}
    post = {
    "username": CREDS["user"],
    "password": CREDS["password"]
    }
    with patch('requests.post') as mock_post:
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = expected
        r = gen_jwt_auth.get_jwt_auth(CREDS)
        mock_post.assert_called_with(CREDS["wp_jwt_auth_url"], json=post)
        assert r == expected


def test_get_jwt_auth_servererror():
    with patch('requests.post') as mock_post:
        mock_response = mock_post.return_value
        mock_response.status_code = 500
        r = gen_jwt_auth.get_jwt_auth(CREDS)
        assert r is None


def test_get_jwt_auth_connectionerror():
    with patch('requests.post') as mock_post:
        mock_post.side_effect = exceptions.ConnectionError
        r = gen_jwt_auth.get_jwt_auth(CREDS)
        assert r is None


def test_get_jwt_auth_timeouterror():
    with patch('requests.post') as mock_post:
        mock_post.side_effect = exceptions.Timeout
        r = gen_jwt_auth.get_jwt_auth(CREDS)
        assert r is None
