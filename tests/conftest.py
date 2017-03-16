import json
import os
import pytest
import responses

from pryke import Pryke
from tests import add_response


@pytest.fixture(scope="session")
def pryke():
    return Pryke("", "", access_token="blah")


@pytest.fixture(scope="session")
@responses.activate
def account(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR')
    return pryke.account('IEAGIITR')


@pytest.fixture(scope="session")
@responses.activate
def attachment(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/attachments/IEAGIITRIYACEGSL')
    return pryke.attachment('IEAGIITRIYACEGSL')


@pytest.fixture(scope="session")
@responses.activate
def comment(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/comments/IEAGIITRIMBEVLZE')
    return pryke.comment('IEAGIITRIMBEVLZE')


@pytest.fixture(scope="session")
@responses.activate
def folder(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/folders/IEAGIITRI4AYHYMV')
    return pryke.folder('IEAGIITRI4AYHYMV')


@pytest.fixture(scope="session")
@responses.activate
def group(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/groups/KX7ZHLB5')
    return pryke.group('KX7ZHLB5')


@pytest.fixture(scope="session")
@responses.activate
def task(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6')
    return pryke.task('IEAGIITRKQAYHYM6')
