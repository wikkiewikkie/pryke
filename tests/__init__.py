import os
import responses


def add_response(request_type, url):

    path = url.replace("https://www.wrike.com/", "")
    path = path.split("/")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', *path)
    path += ".json"

    with open(path, "r") as body_file:
        body = body_file.read()

    responses.add(
        request_type,
        url,
        body=body,
        status=200,
        content_type="application/json"
    )
