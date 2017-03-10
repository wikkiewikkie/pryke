from pryke import Attachment, Folder, User


def test_folder_attachments(mocked):
    """
    attachments method of Folder object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    f = mocked.folder('IEAGIITRI4AYHYMV')

    for attachment in f.attachments():
        assert isinstance(attachment, Attachment)

    assert attachment.id == "IEAGIITRIYACEGSM"


def test_folder_children(mocked):
    """
    children method of Folder object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    f = mocked.folder('IEAGIITRI4AYHYMV')

    for count, child in enumerate(f.children(), start=1):
        assert isinstance(child, Folder)
    assert child.id == "IEAGIITRI4AYHYMX"
    assert count == 2


def test_folder_repr(mocked):
    """
    __repr__ method of Folder object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    f = mocked.folder('IEAGIITRI4AYHYMV')

    assert "Folder" in repr(f)
    assert f.id in repr(f)


def test_folder_shared_users(mocked):
    """
    shared_users method of Folder object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    f = mocked.folder('IEAGIITRI4AYHYMV')

    for u in f.shared_users():
        assert isinstance(u, User)
    assert u.id == "KUAJ25LD"