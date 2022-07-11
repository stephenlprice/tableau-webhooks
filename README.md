# Tableau Webhooks & Twilio

A project demonstrating the use of Tableau's [Webhooks API](https://www.tableau.com/developer/tools/webhook-api) and [Twilio](https://www.twilio.com/) to send notifications to a site or server administrator upon failed data source refreshes.

The app is capable of sending SMS, WhatsApp and perform phone calls when certain events take place on a Tableau Server or Tableau Online site.

![tableau + twilio](assets/images/tableau+twilio.png)

</br>

## Table of Contents
- [Tableau Webhooks & Twilio](#tableau-webhooks--twilio)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Environment Variables](#environment-variables)
  - [Local Usage](#local-usage)
  - [Postman Collection](#postman-collection)
    - [Environment file](#environment-file)
    - [Authentication](#authentication)
  - [Deployment](#deployment)
    - [Steps](#steps)

</br>

## Requirements

This list covers requirements for local development and deployment to Heroku

- [Python](https://www.python.org/) version 3.8.8
- [Anaconda](https://www.anaconda.com/) (optional but recommended)
- Tableau Server or Tableau Online site (a developer site is available for free by signing up for the [developer program](https://www.tableau.com/developer))
- Authentication for Tableau is done via PAT (personal access token) see the documentation for the [Webhooks API](https://help.tableau.com/current/developer/webhooks/en-us/)
- [Twilio](https://www.twilio.com/) account providing a phone number (a trial account is enough)
- [Twilio WhatsApp Sandbox](https://www.google.com/url?q=https://www.twilio.com/console/messaging/whatsapp/sandbox) (obtained on the Twilio console)
- [Postman](https://www.postman.com/) to make requests to the [Tableau Webhooks API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_webhooks.htm) (optional)

</br>

## Installation

1. Clone this repository
```bash
git clone https://github.com/stephenlprice/tableau-twilio-webhooks.git

# navigate inside the project directory
cd tableau-twilio-webhooks
```
2. Create a `conda` environment to install all dependencies and activate it
```bash
# will create an environment called tableau-webhooks
conda env create -f environment.yml

# activates the environment
conda activate tableau-webhooks
```
> ##### *__NOTE__: if you are not using `conda` you can create a `requirements.txt` file or install dependencies manually with `pip3`.*
</br>

1. Create a `.env` file in the project's root directory and add values for each environment variable described in the [example file](#environment-variables) (`example-env`)
```bash
# create the .env file
touch .env
```
> ##### *__NOTE__: the server will have a `RuntimeError` if these environment variables are not accessible.*
</br>

1. Run the app locally with gunicorn
```bash
# $(MODULE_NAME) is notifier and $(VARIABLE_NAME) is app (see notifier.py)
gunicorn notifier:app
```

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

</br>

## Environment Variables

To protect private data such as phone numbers and Tableau passwords, this project relies on `environment variables` to store this information without pushing them to the public Github repository (via `.gitignore`). If you are new to this concept I highly recommend that you read [Twilio's blog post](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) on the subject.

**tldr**: create a `.env` file using the example-env file provided with the repo. `python-dotenv` will load these variables into `notifier.py` to be used in the app.

```bash
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

</br>

## Local Usage

The app was built in [Python](https://www.python.org/) using the [Flask](https://palletsprojects.com/p/flask/) micro web framework. `Flask` can be run on it's own for development purposes however, this is not recommended for production and instead a WSGI server such as [gunicorn](https://gunicorn.org/) is required.

To start the server with `gunicorn` you can run this command:

```bash
# $(MODULE_NAME) is notifier and $(VARIABLE_NAME) is app (see notifier.py)
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

</br>

## Postman Collection

![postman logo](assets/images/postman.png)

This repository contains a [Postman](https://www.postman.com/) collection and environment file to help you interact with [Tableau Webhooks API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_webhooks.htm) which is available on either Tableau Server or Tableau Online (*[see requirements](#requirements)*). 

Once you have added a webhook to the Tableau site or server, you can test it using the `test` request provided in the collection. It is also useful to get a `list` of webhooks registered on the server to get the ID of a webhook that you wish to test.

### Environment file

The collection was built to leverage the provided environment file which will store useful information such as credentials and URLs as well as allowing scripts to update variables for you automatically.

> ##### *__WARNING__: Do not push usernames, passwords or personal access tokens to Github as they will be accessible by crawlers and is a well known security risk. You can fork environment files for local use and keep an empty template available on the repository for others to use.*
</br>

### Authentication

To make requests to Tableau's RESTful endpoints you will need to authenticate by way of a username & password or via PAT (personal access token) to obtain an `API key` that allows users to make requests to other endpoints. 

The collection has a `prerequest script` that will automatically run an authentication request every time you make any other request and therefore saves you from having to do this manually. This functionality requires that you provide username, password and PAT values in the provided environment file.

</br>

## Deployment

![production deployment](assets/images/flask-gunicorn.png)
<h6><i><strong>Source</strong>: <a href="https://eserdk.medium.com/heroku-nginx-gunicorn-flask-f10e81aca90d">Medium: Configuring heroku-based nginx and gunicorn to serve static content and to pass requests directly to the app</a></i></h6>

</br>

The app is setup for deployment on [Heroku](https://heroku.com/) using a free dyno (database not required). Deployment to this platform has a few requirements:

- Free [Heroku](https://heroku.com/) account
- Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- An `environment.yml` or `requirements.txt` file
- A `Procfile`
- Heroku buildpacks for [conda](https://elements.heroku.com/buildpacks/pl31/heroku-buildpack-conda) or [python](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python)

### Steps

1. Add a [Heroku remote](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote) (track this git repo on a Heroku app)
```bash
# creates a new app (declare a name or it will be randomly named)
heroku create your-app-name

# add an existing Heroku remote to the git repo
heroku git:remote -a your-app-name

# confirm that a Heroku remote is tracking the repo
git remote -v
```

2. Add a buildpack to this Heroku app ([conda](https://elements.heroku.com/buildpacks/pl31/heroku-buildpack-conda) or [python](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python))
```bash
# conda buildpack (community built)
heroku buildpacks:set https://github.com/pl31/heroku-buildpack-conda.git

# python buildpack (offical buildpack)
heroku buildpacks:set https://github.com/heroku/heroku-buildpack-python.git
```

3. The existing `Procfile` runs the command launch a "web" dyno on Heroku
```bash
web: gunicorn notifier:app
```

4. Projects using `conda` environments can use the provided `environment.yml` file, otherwise you will have to create a `requirements.txt` file to install [python dependencies on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#declare-app-dependencies)

5. Add all of the [environment variables](#environment-variables) listed in the `example-env` file to the Heroku app's settings under "config vars" (this is done on the website)
   
> ##### *__NOTE__: the server will have a `RuntimeError` if these environment variables are not accessible.*
</br>

6. Deploy [code to Heroku](https://devcenter.heroku.com/articles/git#deploying-code) 
```bash
git push heroku main
```
