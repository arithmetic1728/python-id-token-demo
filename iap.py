from google.auth.transport.requests import Request
from google.auth import jwt
from google.oauth2 import id_token
import requests


def make_request_to_iap():
    url = "https://print-iap-jwt-assertion-dot-cloud-iap-for-testing.uc.r.appspot.com"
    audience = (
        "1031437410300-ki5srmdg37qc6cl521dlqcmt4gbjufn5.apps.googleusercontent.com"
    )

    oidc_token = id_token.fetch_id_token(Request(), audience)

    resp = requests.request(
        "GET", url, headers={"Authorization": "Bearer {}".format(oidc_token)}
    )

    iap_token = resp.text
    print(iap_token)

    return iap_token


def verify_iap_token(token):
    resp = requests.get("https://www.gstatic.com/iap/verify/public_key")
    keys = resp.json()

    decoded_jwt = jwt.decode(
        token, certs=keys, audience="/projects/1031437410300/apps/cloud-iap-for-testing"
    )
    print(decoded_jwt)


iap_token = make_request_to_iap()
verify_iap_token(iap_token)
