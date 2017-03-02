from pryke import Folder, Pryke


def test_pryke(keys):

    p = Pryke(keys['client_id'],
              keys['client_secret'],
              access_token=keys['access_token'])

    assert isinstance(p, Pryke)


def test_pryke_folders(pryke):
    for folder in pryke.folders():
        assert isinstance(folder, Folder)
