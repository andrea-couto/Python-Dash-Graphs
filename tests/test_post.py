import pytest
import push_data_quick
import requests


def test_establish_web_response():
    assert push_data_quick.establish_web_response\
               ('https://hn.algolia.com/api/v1/search_by_date?query=%22Ask%20HN%20:%20Who%20is%20hiring%3F%22&'
                'hitsPerPage=100&numericFilters=created_at_i>1454338862') is not None


def test_missing_url_parts():
    with pytest.raises(requests.exceptions.MissingSchema):
        push_data_quick.establish_web_response('badurl')


def test_url_incorrect():
    with pytest.raises(requests.exceptions.ConnectionError):
        push_data_quick.establish_web_response('https://badurl123.com')