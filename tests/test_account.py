from pryke import Contact, Task


def test_account_contacts(mocked):
    a = mocked.account('IEAGIITR')
    for contact in a.contacts():
        c = contact
        assert isinstance(contact, Contact)
    assert c.id == "KX7ZHLB6"


def test_account_tasks(mocked):
    a = mocked.account('IEAGIITR')
    for task in a.tasks():
        t = task
        assert isinstance(task, Task)
    assert t.id == "IEAGIITRKQAYHYM4"
