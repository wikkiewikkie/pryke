from pryke import Contact, Group, Task


def test_account_contacts(mocked):
    a = mocked.account('IEAGIITR')
    for contact in a.contacts():
        c = contact
        assert isinstance(contact, Contact)
    assert c.id == "KX7ZHLB6"


def test_account_groups(mocked):
    a = mocked.account('IEAGIITR')
    for group in a.groups():
        assert isinstance(group, Group)
    assert group.id == "KX7ZHLB5"


def test_account_tasks(mocked):
    a = mocked.account('IEAGIITR')
    for task in a.tasks():
        t = task
        assert isinstance(task, Task)
    assert t.id == "IEAGIITRKQAYHYM4"
