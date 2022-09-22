import os
from dotenv import load_dotenv
from flask import Flask, request
from modules import broadcast
from utils import environment, log

# load environment files from .env
load_dotenv(".env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

# validate environment variables
environment.validate(env_dict)

# initiate the Flask instance
app = Flask(__name__)

# updates broadcast views when workbooks refreshes trigger a webhook
@app.route("/broadcast-update", methods=["POST"])
def updateBroadcast():
  if request.method == "POST":
    log.logger.info(f"Broadcast workbook updated: {request}")
    # request objects lacking this key automatically raise a KeyError and a 400 Bad Request response
    workbook_id = request.form["resource_luid"]

    try:
      # pushes updates to broadcast if webhook payload workbook id matches an existing broadcast id
      broadcast.update(env_dict, workbook_id)
    except Exception as error:
      log.logger.error("Cannot update Broadcast: ", error)
      return "500 INTERNAL SERVER ERROR", 500
    else:
      return "202 ACCEPTED", 202

  else:
    # any other methods are not supported
    log.logger.error("400 BAD REQUEST: HTTP method not supported")
    return "400 BAD REQUEST: HTTP method not supported", 400

# sends notifications for failed workbook refreshes
@app.route("/workbook-refresh-fail", methods=["POST"])
def notify():
  if request.method == "POST":  
    return "200 SUCCESS"

  else:
    # any other methods are not supported
    log.logger.error("400 BAD REQUEST: HTTP method not supported")
    return "400 BAD REQUEST: HTTP method not supported", 400

if __name__ == "__main__":
  app.run()
