from pryke import Folder, Task, User
from tests import add_response
import responses


@responses.activate
def test_comment_author(comment):
    """
    author method of Comment object.

    Args:
        comment (pryke.Comment):  Comment to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/users/KUAJ25LD')
    assert isinstance(comment.author, User)
    assert comment.author.id == 'KUAJ25LD'


@responses.activate
def test_comment_folder(pryke):
    """
    task method of Comment object.

    Args:
        comment (pryke.Comment):  Comment to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/comments/IEAGIITRIMBEVLZD')
    add_response(responses.GET, 'https://www.wrike.com/api/v3/folders/IEAGIITRI4AYHYMV')
    comment = pryke.comment("IEAGIITRIMBEVLZD")
    assert isinstance(comment.folder, Folder)
    assert comment.folder.id == 'IEAGIITRI4AYHYMV'
    assert comment.task is None


@responses.activate
def test_comment_task(comment):
    """
    task method of Comment object.

    Args:
        comment (pryke.Comment):  Comment to test.
    """
    add_response(responses.GET, 'https://www.wrike.com/api/v3/tasks/IEAGIITRKQAYHYM6')
    assert isinstance(comment.task, Task)
    assert comment.task.id == 'IEAGIITRKQAYHYM6'
    assert comment.folder is None
