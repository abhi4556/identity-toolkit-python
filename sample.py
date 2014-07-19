from flask import Flask, make_response, render_template, request

# Import the helper functions
import gitkitclient

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

