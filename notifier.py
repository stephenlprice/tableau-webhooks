import os, sys
from flask import Flask, request, redirect, url_for
import tableauserverclient as TSC
from tableauserverclient.models.pagination_item import PaginationItem

# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

app = Flask(__name__)

# an API index listing supported endpoints and methods
@app.route("/")
def index():
    return '<h1>API Index</h1>\n<ul><li>/notifier POST - receives incoming Tableau Server webhooks to create datasource failure notifications</li></ul>'

@app.route("/notifier", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
      # dictionary with required environment variables
      env_vars = ["TABLEAU_PAT_NAME", "TABLEAU_PASSWORD", "TABLEAU_SITENAME", "TABLEAU_SERVER"]
      # check that each environment variable is available, else throw an exception
      for vars in env_vars:
        try:
            # check the local dictionary pulled from os.environ
            env_dict[vars]
        except KeyError:
          # output the first environment variable to fail
          print(f"Please set the environment variable {vars}")
          sys.exit(1)

        # creates an authorization object using environment variables
        tableauAuth = TSC.PersonalAccessTokenAuth(env_dict["TABLEAU_PAT_NAME"], env_dict["TABLEAU_PASSWORD"], env_dict["TABLEAU_SITENAME"])
        # server object using environment variables
        server = TSC.Server(env_dict["TABLEAU_SERVER"])
        # server object signs in and fetches a list of datasources
        with server.auth.sign_in(tableauAuth):
          allDatasources, PaginationItem = server.datasources.get()
        
        # loop through datasources on site to output an individual detail
        for dataSource in allDatasources:
          msgStr = f"Datasource Refresh failed\n\tName:{dataSource.name}\n\tDescription:{dataSource.description}\n\tLast updated: {dataSource.updated_at}\n"
          with open("log.txt", "a") as logFile:
            logFile.write(msgStr)

        # return f"POST data: {request.values}"
        return "<h1>Working</h1>"


    else:
      # redirects to index "/" to display a list of supported API endpoints
      return redirect(url_for("index"))

if __name__ == "__main__":
  app.run()
