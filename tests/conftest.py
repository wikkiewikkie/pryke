import pytest

from pryke import Pryke


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
