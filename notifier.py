import os
from flask import Flask, request
import tableauserverclient as TSC
from tableauserverclient.models.pagination_item import PaginationItem

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello, World!'

@app.route("/notifier", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
      # creates an authorization object using environment variables
      tableauAuth = TSC.PersonalAccessTokenAuth(os.environ["TABLEAU_PAT_NAME"], os.environ["TABLEAU_PASSWORD"], os.environ["TABLEAU_SITENAME"])
      # server object using environment variables
      server = TSC.Server(os.environ["TABLEAU_SERVER"])
      # server object signs in and fetches a list of datasources
      with server.auth.sign_in(tableauAuth):
        allDatasources, PaginationItem = server.datasources.get()

      # return f"POST data: {request.values}"
      return "<h1>Working</h1>"

    else: # Debugging
      # return f"GET data: {request.values}"
      return "<h1>Working</h1>"

if __name__ == "__main__":
  app.run()
