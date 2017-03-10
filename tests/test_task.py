from pryke import Account, Attachment, Task


def test_task_account(mocked):
    """
    account method of Task object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    t = mocked.task('IEAGIITRKQAYHYM6')
    assert isinstance(t.account, Account)
    assert t.account.id == 'IEAGIITR'

    t = Task(mocked)
    assert t.account is None


def test_task_attachments(mocked):
    """
    attachments method of Task object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    t = mocked.task('IEAGIITRKQAYHYM6')

    for attachment in t.attachments():
        assert isinstance(attachment, Attachment)

    assert attachment.id == "IEAGIITRIYACEGSN"
    assert attachment.task_id == 'IEAGIITRKQAYHYM6'


def test_task_repr(mocked):
    """
    __repr__ method of Task object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    t = mocked.task('IEAGIITRKQAYHYM6')
    value = repr(t)
    assert "Task" in value
    assert t.id in value
