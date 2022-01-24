from flask import Flask, redirect, session, url_for
from authlib.integrations.flask_client import OAuth

from apple import ApplePrivateKeyJWT
import config

app = Flask(__name__)
app.secret_key = 'dummy secret key'
app.config.from_object('config')

oauth = OAuth(app)
oauth.register(
    name='apple',
    # response_mode must be form_post when name or email scope is requested, as required by Apple:
    authorize_params={'response_mode': 'form_post'},
    token_endpoint_auth_method=ApplePrivateKeyJWT(apple_private_key=config.APPLE_PRIVATE_KEY,
                                                  apple_key_id=config.APPLE_KEY_ID,
                                                  apple_team_id=config.APPLE_TEAM_ID),
    client_kwargs={'scope': 'openid email name'}
)


@app.route('/')
def index():
    email = session.get('email')
    return {'email': email}, 200


@app.route('/auth/apple')
def login():
    redirect_uri = url_for('callback', _external=True)
    return oauth.apple.authorize_redirect(redirect_uri)


@app.route('/auth/apple/callback', methods=['POST'])
def callback():
    token = oauth.apple.authorize_access_token()
    userinfo = token.get('userinfo')
    if userinfo and userinfo.get('email_verified'):
        session['email'] = userinfo['email']
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
