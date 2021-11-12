from flask import Flask, request

app = Flask(__name__)

@app.route("/notifier", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
      # return f"POST data: {request.values}"
      return "<h1>Working</h1>"

    else: # Debugging
      # return f"GET data: {request.values}"
      return "<h1>Working</h1>"

if __name__ == "__main__":
  app.run()
