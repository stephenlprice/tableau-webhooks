from flask import Flask, request

app = Flask(__name__)

@app.route("/notifier", methods=["GET", "POST"])
def notify():
    if request.method == "POST":
      return f"POST data: {request.values}"
    
    else: # Debugging
      return f"GET data: {request.values}"

if __name__ == "__main__":
  app.run()
