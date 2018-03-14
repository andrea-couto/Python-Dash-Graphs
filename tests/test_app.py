import app
import pytest


def test_get_database():
    assert app.get_database('https://hackernewsgraphs.firebaseio.com/') is not None


def test_invalid_get_database():
    with pytest.raises(SystemExit):
        app.get_database('https://hackernewsgraphs123.firebaseio.com/')
