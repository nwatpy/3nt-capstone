from requests import exceptions
from unittest.mock import patch
from requests.auth import HTTPBasicAuth
import base64
import pyblog

CREDS = {
    "wp_posts_url": "http://18.189.31.189:8088/wp-json/wp/v2/posts",
    "user": "test_user",
    "password": "test_password"
}

def test_get_wp_response_success():
    expected = []
    with patch('requests.get') as mock_get:
        credentials = CREDS["user"] + ':' + CREDS["password"]
        token = base64.b64encode(credentials.encode())
        header = {'Authorization': 'Basic ' + token.decode('utf-8')}
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = expected
        response_data = pyblog.get_wp_response(CREDS)
        mock_get.assert_called_with(CREDS['wp_posts_url'], headers=header)
        assert response_data == expected

