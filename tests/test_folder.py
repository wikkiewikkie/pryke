from pryke import Attachment, Folder, User
from tests import add_response

import responses


@responses.activate
def test_folder_attachments(folder):
    """
    attachments method of Folder object.

    Args:
        folder (Folder):  Folder object to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/folders/IEAGIITRI4AYHYMV/attachments')

    for attachment in folder.attachments():
        assert isinstance(attachment, Attachment)
    assert attachment.id == "IEAGIITRIYACEGSM"


def test_folder_children(folder):
    """
    children method of Folder object.

    Args:
        folder (Folder):  Folder object to test.
    """
    for count, child in enumerate(folder.children(), start=1):
        assert isinstance(child, Folder)
    assert child.id == "IEAGIITRI4AYHYMX"
    assert count == 2


def test_folder_repr(folder):
    """
    __repr__ method of Folder object.

    Args:
        folder (Folder):  Folder object to test.
    """
    assert "Folder" in repr(folder)
    assert folder.id in repr(folder)


@responses.activate
def test_folder_shared_users(folder):
    """
    shared_users method of Folder object.

    Args:
        folder (Folder):  Folder object to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/users/KUAJ25LD')

    for u in folder.shared_users():
        assert isinstance(u, User)
    assert u.id == "KUAJ25LD"
