# Tableau & Twilio via Webhooks

A project demonstrating the use of Tableau's [Webhooks API](https://www.tableau.com/developer/tools/webhook-api) and [Twilio](https://www.twilio.com/) to send notifications to a site or server administrator upon failed data source refreshes.

The app is capable of sending SMS, WhatsApp and perform phone calls when certain events take place on a Tableau Server or Tableau Online site.

![webhook description](assets/images/webhooks-vs-apis.png)
##### *source: [CleverTap: What Are Webhooks? And Why Should You Get Hooked?](https://clevertap.com/blog/what-are-webhooks/)*

</br>

## Dependencies

This project was built with [Anaconda](https://www.anaconda.com/), therefore the development environment can be cloned from the `environment.yml` file. Most dependencies are installed with `conda` while the last three are installed with `pip3`. 

If you are new to `conda` I recommend keeping the [conda cheatsheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf) nearby for reference.

```yaml
name: tableau-twilio
channels:
  - defaults
dependencies:
  - python=3.8.8
  - flask=2.0.2
  - gunicorn=20.1.0
  - pip=21.2.4
  - pip:
    - python-dotenv==0.19.2
    - twilio==7.3.0
    - tableauserverclient==0.17.0
prefix: /Users/stephenlprice/anaconda3/envs/tableau-twilio
```

It is possible to recreate this environment without Anaconda, using something like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). In that case you can install all dependencies with `pip3` and write a `requirements.txt` file to document your dependencies.

## Environment Variables

To protect private data such as phone numbers and Tableau passwords, this project relies on `environment variables` to store this information without pushing them to the public Github repository (via `.gitignore`). If you are new to this concept I highly recommend that you read [Twilio's blog post](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) on the subject.

**tldr**: create a `.env` file using the example-env file provided with the repo. `python-dotenv` will load these variables into `notifier.py` to be used in the app.

```.env
TABLEAU_PAT_NAME=your-token-name
TABLEAU_PASSWORD=your-token-password
TABLEAU_SITENAME=your-sitename
TABLEAU_SERVER=your-tableau-server-online-domain
TWILIO_ACCOUNT_SID=your-twilio-account
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_FROM_NUMBER=+1your-twilio-number
TWILIO_TO_NUMBER=+1your-number
WHATSAPP_FROM=whatsapp:+1your-twilio-whatsappsandbox-number
WHATSAPP_TO=whatsapp:+1your-whatsapp-number
```

## Local Usage

The app was built in [Python](https://www.python.org/) using the [Flask](https://palletsprojects.com/p/flask/) micro web framework. `Flask` can be run on it's own for development purposes however, this is not recommended for production and instead a WSGI server such as [gunicorn](https://gunicorn.org/) is required.

To start the server with `gunicorn` you can run this command:

```bash
gunicorn notifier:app
```

As a result `gunicorn` will log activity made to the app's endpoints and will be available at: 

```bash
# API index
http://127.0.0.1:8000
# the endpoint used for notifications
http://127.0.0.1:8000/notifier
```

You can trigger Twilio notifications by making a POST request to the `/notifier` endpoint such as:

```bash
curl "http://127.0.0.1:8000/notifier" -X POST
```

## Deployment

![production deployment](assets/images/flask-gunicorn.png)
##### *source: [Medium: Configuring heroku-based nginx and gunicorn to serve static content and to pass requests directly to the app](https://eserdk.medium.com/heroku-nginx-gunicorn-flask-f10e81aca90d)*

</br>

The app is setup for deployment on [Heroku](https://heroku.com/) using a free dyno (database no required). Deployment to this platform has a few requirements:

- [ ] Free [Heroku](https://heroku.com/) account
- [ ] The [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [ ] An `environment.yml` file
- [ ] A `Procfile`
- [ ] Heroku buildpacks for [conda](https://elements.heroku.com/buildpacks/pl31/heroku-buildpack-conda) or [python](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python)








