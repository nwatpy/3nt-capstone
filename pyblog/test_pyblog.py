from requests import exceptions
from unittest.mock import patch
import pyblog

CREDS = {
    "wp_posts_url": "http://18.189.31.189:8088/wp-json/wp/v2/posts",
    "user": "test_user",
    "password": "test_password",
    "jwt_auth": "test_auth_token"
}


def test_get_wp_r_success():
    expected = []
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = expected
        r = pyblog.get_wp_r(CREDS)
        mock_get.assert_called_with(
            CREDS["wp_posts_url"], auth=(CREDS["user"], CREDS["password"]))
        assert r == expected


def test_get_wp_r_servererror():
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 500
        r = pyblog.get_wp_r(CREDS)
        assert r is None


def test_get_wp_r_connectionerror():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = exceptions.ConnectionError
        r = pyblog.get_wp_r(CREDS)
        assert r is None


def test_get_wp_r_timeouterror():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = exceptions.Timeout
        r = pyblog.get_wp_r(CREDS)
        assert r is None

def test_wp_publish_success():
    curHeaders = {
        "Authorization": "Bearer %s" % CREDS["jwt_auth"],
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    post = {}
    with patch('requests.post') as mock_post:
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        r = pyblog.wp_publish(CREDS, post)
        mock_post.assert_called_with(CREDS["wp_posts_url"], headers=curHeaders, json=post)
        if not mock_response.status_code == 201:
            assert "Post failed.\
            Possible issue with connection or credentials."
        else:
            assert "Data successfully posted to wordpress."