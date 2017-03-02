import json
import os
import pytest

from pryke import Pryke


class MockOAuthSession:
    def __init__(self):
        self.client_id = None
        self.redirect_uri = None
        self.token = None
        self.access_token = None

    @property
    def authorized(self):
        return True

    def get(self, url):
        path = url.replace("https://www.wrike.com/", "")
        path = path.split("/")
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', *path)
        path += ".json"
        return MockOAuthResponse(path)


class MockOAuthResponse(object):

    def __init__(self, path):
        self._path = path

    def json(self):
        with open(self._path, "r") as json_file:
            data = json.load(json_file)
            return data

    @property
    def status_code(self):
        if os.path.exists(self._path):
            return 200
        else:
            return 404


def pytest_addoption(parser):
    parser.addoption("--clientid", action="store", help="Client ID")
    parser.addoption("--clientsecret", action="store", help="Client Secret")
    parser.addoption("--accesstoken", action="store", help="Access Token")


@pytest.fixture(scope="session")
def keys(request):
    k = dict()
    k['client_id'] = request.config.getoption("--clientid")
    k['client_secret'] = request.config.getoption("--clientsecret")
    k['access_token'] = request.config.getoption("--accesstoken")
    return k


@pytest.fixture(scope="session")
def pryke(keys):
    return Pryke(keys['client_id'], keys['client_secret'], access_token=keys['access_token'])


@pytest.fixture(scope="session")
def mocked():
    p = Pryke(None, None, "fake")
    p.oauth = MockOAuthSession()
    return p