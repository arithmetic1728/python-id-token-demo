from google.auth.transport.requests import Request
from google.auth import jwt
from google.oauth2 import id_token
import requests


def make_request_to_iap():
    # The IAP url we want to send request.
    iap_url = (
        "https://print-iap-jwt-assertion-dot-cloud-iap-for-testing.uc.r.appspot.com"
    )

    # Use the fetch_id_token method from id_token module in google-auth library
    # to obtain an id token.
    audience = (
        "1031437410300-ki5srmdg37qc6cl521dlqcmt4gbjufn5.apps.googleusercontent.com"
    )
    oidc_token = id_token.fetch_id_token(Request(), audience)

    # Insert id_token to the Authorization header, and send request to IAP url.
    resp = requests.request(
        "GET", iap_url, headers={"Authorization": "Bearer {}".format(oidc_token)}
    )

    # IAP url will return us an IAP token.
    iap_token = resp.text
    print(iap_token)

    return iap_token


def verify_iap_token(iap_token):
    # Fetch the certificates.
    resp = requests.get("https://www.gstatic.com/iap/verify/public_key")
    certs = resp.json()

    # Use decode function from jwt module in google-auth library to verify the
    # token signature, audience etc.
    # The certs argument could be a dictionary of certs or a single cert. In
    # case of a dictionary certs, the function picks the right cert based on the
    # key id in token header.
    decoded_jwt = jwt.decode(
        iap_token,
        certs=certs,  # dictionary of certs
        audience="/projects/1031437410300/apps/cloud-iap-for-testing",
    )

    key_id = jwt.decode_header(iap_token).get("kid")
    decoded_jwt = jwt.decode(
        iap_token,
        certs=certs[key_id],  # a single cert
        audience="/projects/1031437410300/apps/cloud-iap-for-testing",
    )

    print(decoded_jwt)


if __name__ == "__main__":
    iap_token = make_request_to_iap()
    verify_iap_token(iap_token)
