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
@app.route("/webhook", methods=["POST"])
def workbook_event():
  if request.method == "POST":

    webhooks.handleEvent(request.get_json(), env_dict)

    return "202 ACCEPTED", 202

  else:
    # any other methods are not supported
    log.logger.error("400 BAD REQUEST: HTTP method not supported")
    return "400 BAD REQUEST: HTTP method not supported", 400


if __name__ == "__main__":
  app.run()
