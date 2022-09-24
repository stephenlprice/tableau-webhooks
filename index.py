import os
from dotenv import load_dotenv
from flask import Flask, request
from modules import webhooks
from utils import environment, log

# load environment files from .env
load_dotenv(".env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

# validate environment variables
environment.validate(env_dict)

# initiate the Flask instance
app = Flask(__name__)

# handles workbook event webhooks
@app.route("/workbook", methods=["POST"])
def workbook_event():
  if request.method == "POST":
    try:
      webhooks.workbook(request.form, env_dict)
    except Exception as error:
      log.logger.error("Cannot Process Webhook Event: ", error)
      return "500 INTERNAL SERVER ERROR", 500
    else:
      # webhooks require a 2xx response else they deactivate after 4 delivery attempt failures
      return "202 ACCEPTED", 202

  else:
    # any other methods are not supported
    log.logger.error("400 BAD REQUEST: HTTP method not supported")
    return "400 BAD REQUEST: HTTP method not supported", 400

# sends notifications for failed workbook refreshes
@app.route("/workbook-refresh-fail", methods=["POST"])
def notify():
  if request.method == "POST":  
    log.logger.info(f"Workbook Refresh Failed: {request}")
    return "200 SUCCESS"

  else:
    # any other methods are not supported
    log.logger.error("400 BAD REQUEST: HTTP method not supported")
    return "400 BAD REQUEST: HTTP method not supported", 400

if __name__ == "__main__":
  app.run()
