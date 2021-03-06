from pryke import Attachment, AttachmentType, Contact, Folder, Group, Task
from tests import add_response

import datetime
import responses


@responses.activate
def test_account_attachments(account):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR/attachments')
    start = datetime.datetime(2016, 10, 2, 16, 10, 47)
    end = datetime.datetime(2016, 10, 3, 16, 10, 47)

    for attachment in account.attachments(start, end):
        assert isinstance(attachment, Attachment)

    assert isinstance(attachment.created_date, datetime.datetime)
    assert isinstance(attachment.size, int)
    assert attachment.type == AttachmentType.WRIKE


@responses.activate
def test_account_contacts(account):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR/contacts')
    for contact in account.contacts():
        assert isinstance(contact, Contact)
    assert contact.id == "KX7ZHLB6"


@responses.activate
def test_account_folders(account):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR/folders')
    for folder in account.folders():
        assert isinstance(folder, Folder)
    assert folder.id == "IEAGIITRI4AYHYMV"


@responses.activate
def test_account_groups(account):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR/groups')
    for group in account.groups():
        assert isinstance(group, Group)
    assert group.id == "KX7ZHLB5"


@responses.activate
def test_account_recycle_bin(account):
    responses.add(responses.GET, "https://www.wrike.com/api/v3/folders/IEAGIITRI7777776",
                  body='{"data": {}}', status=200, content_type="application/json")
    assert isinstance(account.recycle_bin, Folder)
    assert account.instance._response.request.url == 'https://www.wrike.com/api/v3/folders/IEAGIITRI7777776'


def test_account_repr(account):
    """
    __repr__ method of Account object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    assert "Account" in repr(account)
    assert account.id in repr(account)


@responses.activate
def test_account_root_folder(account):
    responses.add(responses.GET, "https://www.wrike.com/api/v3/folders/IEAGIITRI7777777",
                  body='{"data": {}}', status=200, content_type="application/json")
    assert isinstance(account.root_folder, Folder)
    assert account.instance._response.request.url == 'https://www.wrike.com/api/v3/folders/IEAGIITRI7777777'


@responses.activate
def test_account_tasks(account):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR/tasks')
    for task in account.tasks():
        assert isinstance(task, Task)
    assert task.id == "IEAGIITRKQAYHYM4"
