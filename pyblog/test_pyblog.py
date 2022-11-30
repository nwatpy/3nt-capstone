from requests import exceptions
from unittest.mock import patch
from requests.auth import HTTPBasicAuth
import pyblog

creds = {
    "wp_posts_url": "http://18.189.31.189:8088/wp-json/wp/v2/posts",
    "user": "test_user",
    "password": "test_password"
}

def test_get_wp_response_success():
    with patch('requests.get') as mock_get:
        expected = [   {   '_links': {   'about': [   {   'href': 'http://18.189.31.189:8088/wp-json/wp/v2/types/post'}],
                      'author': [   {   'embeddable': True,
                                        'href': 'http://18.189.31.189:8088/wp-json/wp/v2/users/1'}],
                      'collection': [   {   'href': 'http://18.189.31.189:8088/wp-json/wp/v2/posts'}],
                      'curies': [   {   'href': 'https://api.w.org/{rel}',
                                        'name': 'wp',
                                        'templated': True}],
                      'replies': [   {   'embeddable': True,
                                         'href': 'http://18.189.31.189:8088/wp-json/wp/v2/comments?post=1'}],
                      'self': [   {   'href': 'http://18.189.31.189:8088/wp-json/wp/v2/posts/1'}],
                      'version-history': [   {   'count': 0,
                                                 'href': 'http://18.189.31.189:8088/wp-json/wp/v2/posts/1/revisions'}],
                      'wp:attachment': [   {   'href': 'http://18.189.31.189:8088/wp-json/wp/v2/media?parent=1'}],
                      'wp:term': [   {   'embeddable': True,
                                         'href': 'http://18.189.31.189:8088/wp-json/wp/v2/categories?post=1',
                                         'taxonomy': 'category'},
                                     {   'embeddable': True,
                                         'href': 'http://18.189.31.189:8088/wp-json/wp/v2/tags?post=1',
                                         'taxonomy': 'post_tag'}]},
        'author': 1,
        'categories': [1],
        'comment_status': 'open',
        'content': {   'protected': False,
                       'rendered': '\n'
                                   '<p>Welcome to WordPress. This is your '
                                   'first post. Edit or delete it, then start '
                                   'writing!</p>\n'},
        'date': '2022-11-30T18:48:27',
        'date_gmt': '2022-11-30T18:48:27',
        'excerpt': {   'protected': False,
                       'rendered': '<p>Welcome to WordPress. This is your '
                                   'first post. Edit or delete it, then start '
                                   'writing!</p>\n'},
        'featured_media': 0,
        'format': 'standard',
        'guid': {'rendered': 'http://18.189.31.189:8088/?p=1'},
        'id': 1,
        'link': 'http://18.189.31.189:8088/2022/11/30/hello-world/',
        'meta': [],
        'modified': '2022-11-30T18:48:27',
        'modified_gmt': '2022-11-30T18:48:27',
        'ping_status': 'open',
        'slug': 'hello-world',
        'status': 'publish',
        'sticky': False,
        'tags': [],
        'template': '',
        'title': {'rendered': 'Hello world!'},
        'type': 'post'}]
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = expected
    response_data = pyblog.get_wp_response()
    mock_get.assert_called_with(creds["wp_posts_url"])
    assert response_data == expected