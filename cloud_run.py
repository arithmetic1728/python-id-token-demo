from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests


def make_request_to_cloud_run():
    url = "https://protected-resource-gmdw7sut5q-de.a.run.app"
    audience = "https://protected-resource-gmdw7sut5q-de.a.run.app"

    oidc_token = id_token.fetch_id_token(Request(), audience)

    resp = requests.request(
        "GET", url, headers={"Authorization": "Bearer {}".format(oidc_token)}
    )

    print(resp.status_code)


make_request_to_cloud_run()
