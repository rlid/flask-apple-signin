import os

APPLE_SERVER_METADATA_URL = 'https://appleid.apple.com/.well-known/openid-configuration'
APPLE_CLIENT_ID = os.environ.get('APPLE_CLIENT_ID')

APPLE_TEAM_ID = os.environ.get('APPLE_TEAM_ID')
APPLE_KEY_ID = os.environ.get('APPLE_KEY_ID')

APPLE_PRIVATE_KEY = None
with open(os.environ.get('APPLE_KEY_FILE'), 'r') as f:
    APPLE_PRIVATE_KEY = f.read()
