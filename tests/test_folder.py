from pryke import User


def test_folder_shared_users(mocked):
    f = mocked.folder('IEAGIITRI4AYHYMV')

    for u in f.shared_users():
        assert isinstance(u, User)
    assert u.id == "KUAJ25LD"