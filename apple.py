from authlib.jose import jwt
from urllib.parse import urlparse
from authlib.oauth2.rfc7523.assertion import sign_jwt_bearer_assertion
from authlib.common.urls import add_params_to_qs


class ApplePrivateKeyJWT:
    name = 'apple_private_key_jwt'

    def __init__(self, token_endpoint=None, claims=None,
                 apple_private_key=None, apple_key_id=None, apple_team_id=None):
        self.token_endpoint = token_endpoint
        self.claims = claims
        self.apple_private_key = apple_private_key
        self.apple_key_id = apple_key_id
        self.apple_team_id = apple_team_id

    def sign(self, auth, token_endpoint):
        print(f'auth = {auth}')
        print(f'auth.client_id = {auth.client_id}')
        print(f'auth.client_secret = {auth.client_secret}')
        print(f'auth.auth_method = {auth.auth_method}')
        url = urlparse(token_endpoint)
        return sign_jwt_bearer_assertion(
            key=self.apple_private_key,  # private key
            alg='ES256',  # header:alg
            header={'kid': self.apple_key_id},  # header:kid
            issuer=self.apple_team_id,  # payload:iss
            audience=f'{url.scheme}://{url.netloc}',  # payload:aud (= https://appleid.apple.com)
            subject=auth.client_id,  # payload:sub
            claims=self.claims  # payload:other (if any)
        )

    def __call__(self, auth, method, uri, headers, body):
        print(f'auth = {auth}')
        print(f'auth.client_id = {auth.client_id}')
        print(f'auth.client_secret = {auth.client_secret}')
        print(f'auth.auth_method = {auth.auth_method}')
        print(f'method = {method}')
        token_endpoint = self.token_endpoint
        if not token_endpoint:
            token_endpoint = uri

        client_secret = self.sign(auth, token_endpoint)
        decoded_client_secret = jwt.decode(client_secret, key=self.apple_private_key)
        print(f'decoded_client_secret.header = {decoded_client_secret.header}')
        print(f'decoded_client_secret(.payload) = {decoded_client_secret}')
        print(f'decoded_client_secret.options = {decoded_client_secret.options}')
        print(f'decoded_client_secret.params = {decoded_client_secret.params}')

        body = add_params_to_qs(body or '', [
            ('client_id', auth.client_id),
            ('client_secret', client_secret)
        ])
        print(f'uri = {uri}')
        print(f'headers = {headers}')
        print(f'body = {body}')
        return uri, headers, body
