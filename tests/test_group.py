from pryke import Account, Group, User


def test_group_account(mocked):
    g = mocked.group('KX7ZHLB5')
    a = g.account()
    assert isinstance(a, Account)
    assert a.id == "IEAGIITR"

    g = Group(mocked)
    assert g.account() is None


def test_group_users(mocked):
    g = mocked.group('KX7ZHLB5')
    for user in g.users():
        assert isinstance(user, User)
    assert user.id == "KUAJ25LD"
