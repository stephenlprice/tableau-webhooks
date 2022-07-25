import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for
from modules import broadcast
from utils import log, environment

# dictionary with required environment variables
env_vars = [
  "TABLEAU_SERVER",
  "TABLEAU_SITENAME",
  "TABLEAU_RESTAPI_VERSION",
  "TABLEAU_USERNAME",
  "TABLEAU_CA_CLIENT",
  "TABLEAU_CA_SECRET_ID",
  "TABLEAU_CA_SECRET_VALUE",
  "TABLEAU_PAT_NAME",
  "TABLEAU_PAT_SECRET",
  "TWILIO_ACCOUNT_SID",
  "TWILIO_AUTH_TOKEN",
  "TWILIO_FROM_NUMBER",
  "TWILIO_TO_NUMBER",
  "WHATSAPP_FROM",
  "WHATSAPP_TO"
]

# load environment files from .env
load_dotenv("../.env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

# validate environment variables
environment.validate(env_dict, env_vars)
print('SUCCESS: environment validation passed...')
log.logger.info('SUCCESS: environment validation passed...')

# initiate the Flask instance
app = Flask(__name__)

# an API index listing supported endpoints and methods
@app.route("/")
def index():
    return '<h1>Notifier API Index</h1>\n<ul><li>/notifier <strong>POST</strong> - receives incoming Tableau Server webhooks to create datasource failure notifications</li></ul>'

# handles updating views on tableau broadcast once workbooks are refreshed on tableau cloud
@app.route("/broadcast-update", methods=["GET", "POST"])
def broadcast():
  if request.method == "POST":
    print(request)
    # this method updates workbooks published to broadcast
    broadcast.update(env_dict)
    return "200 SUCCESS"

  elif request.method == "GET":
    # GET requests redirects to index "/" to display a list of supported API endpoints
    return redirect(url_for("index"))

  else:
    # any other methods are not supported
    return "400 Bad Request: method not supported"

# handles notifications for failed workbook refreshes
@app.route("/workbook-refresh-fail", methods=["GET", "POST"])
def notify():
  print(request)
  if request.method == "POST":  
  
    return "200 SUCCESS"

  elif request.method == "GET":
    # GET requests redirects to index "/" to display a list of supported API endpoints
    return redirect(url_for("index"))

  else:
    # any other methods are not supported
    return "400 Bad Request: method not supported"

if __name__ == "__main__":
  app.run()
