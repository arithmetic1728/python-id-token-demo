from google.auth.transport.requests import Request
from google.oauth2 import id_token
import requests


def make_request_to_cloud_run():
    # The Cloud Run url we want to send request.
    cloud_run_url = "https://protected-resource-gmdw7sut5q-de.a.run.app"

    # Use the fetch_id_token method from id_token module in google-auth library
    # to obtain an id token.
    audience = "https://protected-resource-gmdw7sut5q-de.a.run.app"
    oidc_token = id_token.fetch_id_token(Request(), audience)

    # Insert id_token to the Authorization header, and send request to cloud run url.
    resp = requests.request(
        "GET", cloud_run_url, headers={"Authorization": "Bearer {}".format(oidc_token)}
    )

    print(resp.status_code)


if __name__ == "__main__":
    make_request_to_cloud_run()
