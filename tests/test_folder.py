from pryke import Attachment, User


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