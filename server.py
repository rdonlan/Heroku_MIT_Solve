from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='xF0YA3HXqbyz4IRrk5OK9PwvjACaKEuL',   
    client_secret='a-1oMb_oJ-l5UNstKUUuqqG6UCL019A9XAJ3JRfMi4lFuOk-jT-EQIV6doFhtoyI',
    api_base_url='billowing-snowflake-1046.us.auth0.com',
    access_token_url='billowing-snowflake-1046.us.auth0.com/oauth/token',
    authorize_url='billowing-snowflake-1046.us.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# /server.py

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://sheltered-sea-40585.herokuapp.com/callback')

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))  

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'xF0YA3HXqbyz4IRrk5OK9PwvjACaKEuL'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))                    	     	      
