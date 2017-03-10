from pryke import Account, Comment, Contact, Folder, Group, Pryke, Task, User

import datetime

#def test_pryke(mocked):
#
#    p = Pryke(keys['client_id'],
#              keys['client_secret'],
#              access_token=keys['access_token'])
#
#    assert isinstance(p, Pryke)


def test_pryke_account(mocked):
    a = mocked.account('IEAGIITR')
    assert isinstance(a, Account)
    assert isinstance(a.id, str)
    assert a.id == "IEAGIITR"
    assert isinstance(a.created_date, datetime.datetime)

    a = mocked.account('BOGUS')
    assert a is None


def test_pryke_accounts(mocked):
    a = None
    for account in mocked.accounts():
        a = account
        assert isinstance(account, Account)
    assert a.id == "IEAGIITR"


def test_pryke_comments(mocked):
    c = None
    for comment in mocked.comments():
        c = comment
        assert isinstance(comment, Comment)
    assert c.id == "IEAGIITRIMBEVLZE"


def test_pryke_contact(mocked):
    c = mocked.contact('KUAJ25LC')
    assert isinstance(c, Contact)
    assert c.id == "KUAJ25LC"


def test_pryke_contacts(mocked):
    c = None
    for contact in mocked.contacts():
        c = contact
        assert isinstance(contact, Contact)
    assert c.id == "KUAJ25LD"


def test_pryke_folder(mocked):
    f = mocked.folder("IEAGIITRI4AYHYMV")
    assert isinstance(f, Folder)

    assert f.id == "IEAGIITRI4AYHYMV"


def test_pryke_folders(mocked):
    f = None
    for folder in mocked.folders():
        f = folder
        assert isinstance(folder, Folder)

    assert f.id == "IEAGIITRI4AYHYMV"


def test_pryke_group(mocked):
    g = mocked.group('KX7ZHLB5')
    assert isinstance(g, Group)
    assert g.id == "KX7ZHLB5"


def test_pryke_task(mocked):
    t = mocked.task('IEAGIITRKQAYHYM6')
    assert isinstance(t, Task)
    assert t.id == 'IEAGIITRKQAYHYM6'


def test_pryke_tasks(mocked):
    t = None
    for task in mocked.tasks():
        t = task
        assert isinstance(task, Task)

    assert t.id == "IEAGIITRKQAYHYM5"


def test_pryke_user(mocked):
    u = mocked.user('KUAJ25LD')
    assert isinstance(u, User)
    assert u.id == "KUAJ25LD"


def test_pryke_version(mocked):
    major, minor = mocked.version
    assert isinstance(major, int)
    assert isinstance(minor, int)
