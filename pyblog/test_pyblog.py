from requests import exceptions
from unittest.mock import patch
import pyblog

CREDS = {
    "wp_posts_url": "http://18.189.31.189:8088/wp-json/wp/v2/posts",
    "user": "test_user",
    "password": "test_password"
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
