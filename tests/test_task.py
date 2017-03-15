from pryke import Account, Attachment, Comment, Task
from tests import add_response

import os
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


@responses.activate
def test_task_comments(task):
    """
    comments method of Task object.

    Args:
        task (pryke.Task):  Task to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6/comments')

    for comment in task.comments():
        assert isinstance(comment, Comment)

    assert comment.id == "IEAGIITRIMBEVLZE"
    assert comment.task_id == 'IEAGIITRKQAYHYM6'


@responses.activate
def test_task_export(task):
    """
    export method of Task object.

    Args:
        task (pryke.Task):  Task to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/users/KUAJ25LD')
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6/attachments')
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6/comments')

    assert task.export("test.html")
    assert os.path.exists("test.html")
    os.remove("test.html")


def test_task_repr(task):
    """
    __repr__ method of Task object.

    Args:
        mocked (Pryke):  Pryke instance with OAuth client mocked.
    """
    value = repr(task)
    assert "Task" in value
    assert task.id in value
