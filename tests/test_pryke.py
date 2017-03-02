from pryke import Folder, Pryke


#def test_pryke(mocked):
#
#    p = Pryke(keys['client_id'],
#              keys['client_secret'],
#              access_token=keys['access_token'])
#
#    assert isinstance(p, Pryke)


def test_pryke_folders(mocked):
    f = None
    for folder in mocked.folders():
        f = folder
        assert isinstance(folder, Folder)

    assert f.id == "IEAGIITRI4AYHYMV"