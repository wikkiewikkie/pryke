from tests import add_response
from pryke import __version__, Account, Attachment, Comment, Contact, Folder, Group, Task, User
from urllib.parse import urlparse

import datetime
import responses
import time


@responses.activate
def test_pryke_account(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR')
    a = pryke.account('IEAGIITR')
    assert isinstance(a, Account)
    assert isinstance(a.id, str)
    assert a.id == "IEAGIITR"
    assert isinstance(a.created_date, datetime.datetime)

    responses.add(responses.GET, 'https://www.wrike.com/api/v3/accounts/BOGUS', status=404)
    a = pryke.account('BOGUS')
    assert a is None


@responses.activate
def test_pryke_accounts(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts')
    for account in pryke.accounts():
        assert isinstance(account, Account)
    assert account.id == "IEAGIITR"

    url = urlparse(pryke._response.url)
    assert url.path == '/api/v3/accounts'


@responses.activate
def test_pryke_attachment(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/attachments/IEAGIITRIYACEGSL')
    a = pryke.attachment('IEAGIITRIYACEGSL')
    assert isinstance(a, Attachment)
    assert isinstance(a.id, str)
    assert a.id == "IEAGIITRIYACEGSL"
    assert isinstance(a.created_date, datetime.datetime)

    responses.add(responses.GET, 'https://www.wrike.com/api/v3/attachments/BOGUS', status=404)
    a = pryke.attachment('BOGUS')
    assert a is None


@responses.activate
def test_pryke_comment(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/comments/IEAGIITRIMBEVLZE')
    a = pryke.comment('IEAGIITRIMBEVLZE')
    assert isinstance(a, Comment)
    assert isinstance(a.id, str)
    assert a.id == "IEAGIITRIMBEVLZE"

    responses.add(responses.GET, 'https://www.wrike.com/api/v3/comments/BOGUS', status=404)
    a = pryke.comment('BOGUS')
    assert a is None


@responses.activate
def test_pryke_comments(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/comments')
    for comment in pryke.comments():
        assert isinstance(comment, Comment)
    assert comment.id == "IEAGIITRIMBEVLZE"


@responses.activate
def test_pryke_contact(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/contacts/KUAJ25LC')
    c = pryke.contact('KUAJ25LC')
    assert isinstance(c, Contact)
    assert c.id == "KUAJ25LC"


@responses.activate
def test_pryke_contacts(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/contacts')
    for contact in pryke.contacts():
        assert isinstance(contact, Contact)
    assert contact.id == "KUAJ25LD"


@responses.activate
def test_pryke_folder(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/folders/IEAGIITRI4AYHYMV')
    f = pryke.folder("IEAGIITRI4AYHYMV")
    assert isinstance(f, Folder)

    assert f.id == "IEAGIITRI4AYHYMV"


@responses.activate
def test_pryke_folders(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/folders')
    for folder in pryke.folders():
        assert isinstance(folder, Folder)
    assert folder.id == "IEAGIITRI4AYHYMV"


def test_pryke_get(pryke):
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add(responses.GET, "https://www.wrike.com/api/v3/folders", body="{}", status=200,
                      content_type="application/json")
        rsps.add(responses.GET, "https://www.wrike.com/api/v3/tasks", body="{}", status=429,
                      content_type="application/json")
        rsps.add(responses.GET, "https://www.wrike.com/api/v3/tasks", body="{}", status=429,
                      content_type="application/json")
        rsps.add(responses.GET, "https://www.wrike.com/api/v3/tasks", body="{}", status=429,
                      content_type="application/json")
        rsps.add(responses.GET, "https://www.wrike.com/api/v3/tasks", body="{}", status=200,
                      content_type="application/json")
        r = pryke.get("folders", params={"cat": "mouse"})
        assert "?cat=mouse" in r.request.url  # params are passed
        start = time.perf_counter()
        r = pryke.get("tasks", params={"dog": "bone"})
        assert 32 > time.perf_counter()-start > 28  # should throttle for ~30 seconds
        assert r.status_code == 200  # eventually succeeds
        assert "?dog=bone" in r.request.url  # params are passed still
        assert "Pryke" in r.request.headers['User-Agent']
        assert __version__ in r.request.headers['User-Agent']


@responses.activate
def test_pryke_group(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/groups/KX7ZHLB5')
    g = pryke.group('KX7ZHLB5')
    assert isinstance(g, Group)
    assert g.id == "KX7ZHLB5"


@responses.activate
def test_pryke_task(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6')
    t = pryke.task('IEAGIITRKQAYHYM6')
    assert isinstance(t, Task)
    assert t.id == 'IEAGIITRKQAYHYM6'


@responses.activate
def test_pryke_tasks(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks')
    t = None
    for task in pryke.tasks():
        t = task
        assert isinstance(task, Task)

    assert t.id == "IEAGIITRKQAYHYM5"


@responses.activate
def test_pryke_user(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/users/KUAJ25LD')
    u = pryke.user('KUAJ25LD')
    assert isinstance(u, User)
    assert u.id == "KUAJ25LD"


@responses.activate
def test_pryke_version(pryke):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/version')
    major, minor = pryke.version
    assert isinstance(major, int)
    assert isinstance(minor, int)
