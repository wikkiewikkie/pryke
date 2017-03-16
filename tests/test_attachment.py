from pryke import Task, User
from tests import add_response
import responses


@responses.activate
def test_attachment_author(attachment):
    """
    author method of Attachment object.

    Args:
        attachment (pryke.Attachment):  Attachment to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/users/KUAJ25LD')
    assert isinstance(attachment.author, User)
    assert attachment.author.id == "KUAJ25LD"


@responses.activate
def test_attachment_task(attachment):
    """
    task method of Attachment object.

    Args:
        attachment (pryke.Attachment):  Attachment to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6')
    assert isinstance(attachment.task, Task)
    assert attachment.task.id == "IEAGIITRKQAYHYM6"
