import pytest
import push_data
import requests
from geotext import GeoText
from geopy.geocoders import Nominatim

geolocator = Nominatim()

mock_comment_text = "Fake Office Space | London, England | Onsite"
mock_pos_locations = [["nyc"], ["san fran", "bar", "baz"], ["san fran", "brisbane"]]
mock_pos_locations_emptylist = [["nyc"],["san fran", "bar", "baz"], [], ["san fran", "brisbane"]]
mock_locations = {"Brisbane": 1, "Paris": 2}
mock_locations_bad_data = {"Brisbane": 1, "Paris": 2, "Growth Developer": 1}

def test_establish_web_response():
    assert push_data.establish_web_response\
               ('https://hn.algolia.com/api/v1/search_by_date?query=%22Ask%20HN%20:%20Who%20is%20hiring%3F%22&'
                'hitsPerPage=100&numericFilters=created_at_i>1454338862') is not None


def test_missing_url_parts():
    with pytest.raises(requests.exceptions.MissingSchema):
        push_data.establish_web_response('badurl')


def test_url_incorrect():
    with pytest.raises(requests.exceptions.ConnectionError):
        push_data.establish_web_response('https://badurl123.com')


def test_geotext():
    places = GeoText(mock_comment_text)
    cities = places.cities
    assert isinstance(cities, list)


def test_remove_values():
    mock_list = ["bar", "bar", "foo"]
    push_data.remove_values(mock_list, "bar")
    assert mock_list == ["foo"]

def test_get_locations():
    locations = push_data.get_locations_for_year(mock_pos_locations)
    assert locations == {"Nyc": 1, "San fran": 2}


def test_get_locations_emptylist():
    locations = push_data.get_locations_for_year(mock_pos_locations_emptylist)
    assert locations == {"Nyc": 1, "San fran": 2}


def test_get_coordinates():
    location_caching = push_data.get_coordinates_for_locations(mock_locations, geolocator)
    assert location_caching == {"Brisbane": (-27.4689682, 153.0234991), "Paris": (48.8566101, 2.3514992)}


def test_get_coordinates_bad_data():
    location_caching = push_data.get_coordinates_for_locations(mock_locations_bad_data, geolocator)
    assert location_caching == {"Brisbane": (-27.4689682, 153.0234991), "Paris": (48.8566101, 2.3514992)}