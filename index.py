import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, url_for
from modules import broadcast
from utils import environment, log, exceptions

# load environment files from .env
load_dotenv(".env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

# validate environment variables
environment.validate(env_dict)

# initiate the Flask instance
app = Flask(__name__)

# an API index listing supported endpoints and methods
@app.route("/")
def index():
  return (
    """
    <h1>Notifier API Index</h1>
    <ul>
      <li>/notifier <strong>POST</strong> - receives incoming Tableau Server webhooks to create datasource failure notifications</li>
    </ul>
    """, 
    200
  )

# handles updating views on tableau broadcast once workbooks are refreshed on tableau cloud
@app.route("/broadcast-update", methods=["GET", "POST"])
def update():
  if request.method == "POST":
    print(request)
    log.logger.info(f"Broadcast updated: {request}")
    workbook_id = ''

    try:
      # this method updates workbooks published to broadcast
      broadcast.update(env_dict, workbook_id)
    except Exception as error:
      # use Flask's built-in logging for HTTP errors
      app.logger.warning("Cannot update Broadcast: ", error)
      return "500 INTERNAL SERVER ERROR", 500
    else:
      return "202 ACCEPTED", 202

  elif request.method == "GET":
    # GET requests redirects to index "/" to display a list of supported API endpoints
    return redirect(url_for("index"))

  else:
    # any other methods are not supported
    return "400 BAD REQUEST: HTTP method not supported", 400

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
