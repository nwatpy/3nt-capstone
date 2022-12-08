from requests import exceptions
from unittest.mock import patch
import pyblog

CREDS = {
    "wp_posts_url": "http://18.189.31.189:8088/wp-json/wp/v2/posts",
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
            CREDS["wp_posts_url"])
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
        mock_post.assert_called_with(
            CREDS["wp_posts_url"], headers=curHeaders, json=post)
        assert r == "Data successfully posted to wordpress."


def test_wp_publish_failure():
    curHeaders = {
        "Authorization": "Bearer %s" % CREDS["jwt_auth"],
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    post = {}
    with patch('requests.post') as mock_post:
        mock_response = mock_post.return_value
        mock_response.status_code = 500
        r = pyblog.wp_publish(CREDS, post)
        mock_post.assert_called_with(
            CREDS["wp_posts_url"], headers=curHeaders, json=post)
        assert r == "Post failed.\
            Possible issue with connection or credentials."


def test_wp_publish_connectionerror():
    post = {}
    with patch('requests.post') as mock_post:
        mock_post.side_effect = exceptions.ConnectionError
        r = pyblog.wp_publish(CREDS, post)
        assert r == "Could not connect to wordpress."


def test_wp_publish_timeouterror():
    post = {}
    with patch('requests.post') as mock_post:
        mock_post.side_effect = exceptions.Timeout
        r = pyblog.wp_publish(CREDS, post)
        assert r == "Could not connect to wordpress."


def test_run_pyblog_specify_blog_data():
    return_string = pyblog.run_pyblog_specify_blog_data()
    assert return_string == "Please specify --blog=read or --blog=write. \
        Please use -h or --help for more information on this tool"


def test_run_write_CLI_main_menu():
    return_string = pyblog.run_write_CLI_main_menu()
    assert return_string == "Please select from the following:\
        title (create title for your post)\
        content (write your post)\
        post (show post data before publishing)\
        publish (post to wordpress)\
        template (publishes designated template file)\
        read (switch to read mode)\
        exit (quit Pyblog CLI)"


def test_run_write_title_menu():
    return_string = pyblog.run_write_title_menu()
    assert return_string == "Provide a title for your post:"


def test_run_write_content_menu():
    return_string = pyblog.run_write_content_menu()
    assert return_string == "Provide content for your post:"


def test_run_write_ask_template_data():
    return_string = pyblog.run_write_ask_template_data()
    assert return_string == "Is template file yaml or plain text?\
    Type yaml or plain:"


def test_run_write_ask_template_filepath():
    return_string = pyblog.run_write_ask_template_filepath()
    assert return_string == "Provide filepath to template:"


def test_run_read_main_menu():
    return_string = pyblog.run_read_main_menu()
    assert return_string == "Choose how to display data:\
        json, yaml\
        write (switch to write mode)\
        exit (quit Pyblog CLI)"


def test_run_read_connection_error():
    return_string = pyblog.run_read_connection_error()
    assert return_string == "Could not connect to wordpress."


def test_run_read_display_json():
    return_string = pyblog.run_read_display_json()
    assert return_string == "Displaying newest post data.\
        Entire response saved to ./data/r.json"


def test_run_read_display_yaml():
    return_string = pyblog.run_read_display_yaml()
    assert return_string == "Displaying newest post data.\
        Entire response saved to ./data/r.yaml\
        Clean response saved to ./data/clean.yaml\
        yaml data displayed saved to ./data/cleaner.yaml"
