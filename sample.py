# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, make_response, render_template, request

# Import the helper functions
from identitytoolkit import gitkitclient

app = Flask(__name__)
app.debug = True

# Import the configuration file you downloaded from Google Developer Console
gitkit_instance = gitkitclient.GitkitClient.FromConfigFile(
      'gitkit-server-config.json')

@app.route("/", methods=['GET', 'POST'])
def index():
  text = "You are not signed in."

  # Check for and read the Google Identity Toolkit token if present
  if 'gtoken' in request.cookies:
    gitkit_user = gitkit_instance.VerifyGitkitToken(request.cookies['gtoken'])
    if gitkit_user:
      text = "Welcome " + gitkit_user.email + "! Your user info is: " + str(vars(gitkit_user))

  response = make_response(render_template('index.html', CONTENT=text))
  response.headers['Content-Type'] = 'text/html'
  return response

@app.route("/widget", methods=['GET', 'POST'])
def signInPage():

  response = make_response(render_template('widget.html'))

  # OPTIONAL (only for Yahoo support): Take information sent by POST request to the sign-in-page and forward it to the Javascript
  #post_body = ''
  #if request.method == 'POST':
  #   post_body = urlencode(request.data)
  #response = make_response(render_template('sign-in-page.html', 
  #                                         POST_BODY=post_body))

  response.headers['Content-Type'] = 'text/html'
  return response

if __name__ == "__main__":
    app.run(port=8000)

