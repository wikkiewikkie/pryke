from pryke import Attachment


def test_task_attachments(mocked):
    """
    attachments method of Folder object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    f = mocked.task('IEAGIITRKQAYHYM6')

    for attachment in f.attachments():
        assert isinstance(attachment, Attachment)

    assert attachment.id == "IEAGIITRIYACEGSN"
    assert attachment.task_id == 'IEAGIITRKQAYHYM6'