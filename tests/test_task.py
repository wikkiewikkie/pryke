from pryke import Account, Attachment, Task
from tests import add_response

import responses


@responses.activate
def test_task_account(task):
    """
    account method of Task object.

    Args:
        task (pryke.Task):  Task to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR')
    assert isinstance(task.account, Account)
    assert task.account.id == 'IEAGIITR'

    # TODO: re-implement
    # t = Task(mocked)
    # assert t.account is None


@responses.activate
def test_task_attachments(task):
    """
    attachments method of Task object.

    Args:
        task (pryke.Task):  Task to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6/attachments')

    for attachment in task.attachments():
        assert isinstance(attachment, Attachment)

    assert attachment.id == "IEAGIITRIYACEGSN"
    assert attachment.task_id == 'IEAGIITRKQAYHYM6'


def test_task_repr(task):
    """
    __repr__ method of Task object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    value = repr(task)
    assert "Task" in value
    assert task.id in value
