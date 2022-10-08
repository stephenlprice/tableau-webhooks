# Tableau Webhooks

This is a Tableau automation server leveraging the [Webhooks API](https://www.tableau.com/developer/tools/webhook-api) to orchestrate processes dependent on events taking place in Tableau Cloud or Tableau Server.

<p align="center">
<img src="assets/images/anne-nygard-viq9Ztqi3Vc-unsplash.jpg" alt="fishing hooks">
</p>


###### IMAGE SOURCE: unsplash.com (Anne Nygard)

</br>

The Webhooks API supports events related to resources such as workbooks, datasources and administrator users. This automation server will receive `POST` requests from your Tableau environment when events take place, allowing you to implement functionality such as being notified via Slack, Twilio or other messaging services as well as automating resource management. To provide automation features, this server is setup to make requests to Tableau's [REST API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm).

</br>

## Table of Contents
- [Tableau Webhooks](#tableau-webhooks)
          - [IMAGE SOURCE: unsplash.com (Anne Nygard)](#image-source-unsplashcom-anne-nygard)
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

This list covers requirements for local development and deployment to Heroku (note that you are free to deploy this server on other platforms).

- [ ] [Python](https://www.python.org/) (*the version is declared in the `environment.yml` file*)
- [ ] [Anaconda](https://www.anaconda.com/) or some other Python environment manager (*optional but recommended*)
- [ ] Tableau Server or a Tableau Cloud site (a developer site is available for free by signing up for the [developer program](https://www.tableau.com/developer))
- [ ] Authentication to Tableau's REST API is performed via `PAT` (*personal access token*), see the documentation for [REST API authentication](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_authentication.htm#sign_in)
- [ ] [Postman](https://www.postman.com/) to make test requests to the [Tableau Webhooks API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_webhooks.htm) or to test the automation server during local development (*optional*)
- [ ] [Request Bin](https://requestbin.com/) a useful and free service you can use to receive real webhooks requests for development (*optional*)

</br>

## Installation

1. Clone this repository
```bash
git clone git@github.com:stephenlprice/tableau-webhooks.git
# or
git clone https://github.com/stephenlprice/tableau-webhooks.git

# navigate inside the project directory
cd tableau-webhooks
```
1. Create a `conda` environment to install all dependencies and activate it (*see [Dependencies](#dependencies) for more info*). To install `conda` on a new machine, refer to the [Anaconda website](https://www.anaconda.com/).
```bash
# will create an environment called tableau-webhooks
conda env create -f environment.yml

# activates the environment
conda activate tableau-webhooks

# lists existing conda environments, adds an asterisk next to the active environment
conda env list
```
> ##### *__NOTE__: if you are not using `conda` you can create a `requirements.txt` file or install the dependencies listed in the `environment.yml` file manually with `pip3`.*
</br>

3. Create a `.env` file in the project's root directory and add values for each environment variable described in the [Environment Variables](#environment-variables) section.
```bash
# create the .env file
touch .env
```
> ##### *__NOTE__: the server will raise a `RuntimeError` if these environment variables are not declared.*
</br>

4. Run the app locally with gunicorn
```bash
# $(MODULE_NAME) is index and $(VARIABLE_NAME) is app (index.py is where the Flask server is initialized)
gunicorn index:app
```

</br>

## Dependencies

This project was built with [Anaconda](https://www.anaconda.com/), therefore the development environment can be cloned from the `environment.yml` file. Most dependencies are installed with `conda` while the last three are installed with `pip3`. 

If you are new to `conda` I recommend keeping the [conda cheatsheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf) nearby for reference.

```yaml
name: tableau-webhooks
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
```

It is possible to recreate this environment without Anaconda, using something like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). In that case you can install all dependencies with `pip3` and write a `requirements.txt` file to document your dependencies.

</br>

## Environment Variables

To protect private data such as phone numbers and passwords, this project relies on `environment variables` to store this information without pushing them to the public Github repository (via `.gitignore`). If you are new to this concept I highly recommend that you read [Twilio's blog post](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) on the subject.

**tldr**: create a `.env` file using the example-env file provided with the repo. `python-dotenv` will load these variables into `notifier.py` to be used in the app.

Your `.env` file must contain all of the following variables:

```bash
TABLEAU_DOMAIN='tableau server or tableau cloud domain'
TABLEAU_SITENAME='tableau sitename'
TABLEAU_RESTAPI_VERSION='tableau rest api version'
TABLEAU_SESSION_MINUTES=240
TABLEAU_USERNAME='tableau username'
TABLEAU_CA_CLIENT='connected app client id'
TABLEAU_CA_SECRET_ID='connected app secret id'
TABLEAU_CA_SECRET_VALUE='connected app secret value'
TABLEAU_PAT_NAME='personal access token name'
TABLEAU_PAT_SECRET='personal access token secret'
TWILIO_ACCOUNT_SID='twilio account'
TWILIO_AUTH_TOKEN='twilio token'
TWILIO_FROM_NUMBER='+1 twilio account phone number'
TWILIO_TO_NUMBER='+1 your phone number'
WHATSAPP_FROM='whatsapp:+1 twilio whatsapp sandbox number'
WHATSAPP_TO='whatsapp:+1 your whatsapp number'
FLASK_ENV='default is production, set to development for debugging'
```

</br>

## Local Usage

The app was built in [Python](https://www.python.org/) using the [Flask](https://palletsprojects.com/p/flask/) micro web framework. `Flask` can run on it's own for development purposes however, this is not recommended for production and instead a WSGI server such as [gunicorn](https://gunicorn.org/) is required.

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

The Postman collection was built to leverage the provided environment file which will store useful information such as credentials and URLs as well as allowing scripts to update variables for you automatically.

> ##### *__WARNING__: Do not push usernames, passwords or personal access tokens to Github as they will be accessible by crawlers and is a well known security risk. You can fork environment files for local use and keep an empty template available on the repository for others to use.*
> 
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
