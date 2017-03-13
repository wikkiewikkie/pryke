from pryke import Account, User
from tests import add_response

import responses


@responses.activate
def test_group_account(group):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/accounts/IEAGIITR')
    a = group.account()
    assert isinstance(a, Account)
    assert a.id == "IEAGIITR"

    # TODO: re-implement
    # g = Group(mocked)
    # assert g.account() is None


@responses.activate
def test_group_users(group):
    add_response(responses.GET, 'https://www.wrike.com/api/v3/users/KUAJ25LD')
    for user in group.users():
        assert isinstance(user, User)
    assert user.id == "KUAJ25LD"
