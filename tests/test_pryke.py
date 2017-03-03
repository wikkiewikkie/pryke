from pryke import Account, Contact, Folder, Pryke, Task


#def test_pryke(mocked):
#
#    p = Pryke(keys['client_id'],
#              keys['client_secret'],
#              access_token=keys['access_token'])
#
#    assert isinstance(p, Pryke)

def test_pryke_accounts(mocked):
    a = None
    for account in mocked.accounts():
        a = account
        assert isinstance(account, Account)
    assert a.id == "IEAGIITR"


def test_pryke_contacts(mocked):
    c = None
    for contact in mocked.contacts():
        c = contact
        assert isinstance(contact, Contact)
    assert c.id == "KUAJ25LD"


def test_pryke_folders(mocked):
    f = None
    for folder in mocked.folders():
        f = folder
        assert isinstance(folder, Folder)

    assert f.id == "IEAGIITRI4AYHYMV"


def test_pryke_tasks(mocked):
    t = None
    for task in mocked.tasks():
        t = task
        assert isinstance(task, Task)

    assert t.id == "IEAGIITRKQAYHYM5"