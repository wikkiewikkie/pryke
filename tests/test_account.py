from pryke import Attachment, AttachmentType, Contact, Folder, Group, Task

import datetime


def test_account_attachments(mocked):
    a = mocked.account('IEAGIITR')
    start = datetime.datetime(2016, 10, 2, 16, 10, 47)
    end = datetime.datetime(2016, 10, 3, 16, 10, 47)

    for attachment in a.attachments(start, end):
        assert isinstance(attachment, Attachment)

    assert isinstance(attachment.created_date, datetime.datetime)
    assert isinstance(attachment.size, int)
    assert attachment.type == AttachmentType.wrike


def test_account_contacts(mocked):
    a = mocked.account('IEAGIITR')
    for contact in a.contacts():
        c = contact
        assert isinstance(contact, Contact)
    assert c.id == "KX7ZHLB6"


def test_account_folders(mocked):
    a = mocked.account('IEAGIITR')
    for folder in a.folders():
        assert isinstance(folder, Folder)
    assert folder.id == "IEAGIITRI4AYHYMV"


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
