# Tableau Webhooks

This is a Tableau automation server leveraging the [Webhooks API](https://www.tableau.com/developer/tools/webhook-api) to orchestrate processes dependent on events taking place in Tableau Cloud or Tableau Server.

<p align="center">
<img src="assets/images/anne-nygard-viq9Ztqi3Vc-unsplash.jpg" alt="fishing hooks">
</p>

<h6><i><strong>Image Source</strong>: <a href="https://unsplash.com/photos/viq9Ztqi3Vc" target="_blank">unsplash.com (Anne Nygård)</a></i></h6>

</br>

The Webhooks API supports events related to resources such as workbooks, datasources and administrator users. This automation server will receive `POST` requests from your Tableau environment when events take place, allowing you to implement functionality such as being notified via Slack, Twilio or other messaging services as well as automating resource management. To provide automation features, this server is setup to make requests to Tableau's [REST API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api.htm).

</br>

## Table of Contents
- [Tableau Webhooks](#tableau-webhooks)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Environment Variables](#environment-variables)
  - [Local Usage](#local-usage)
  - [Postman Collection](#postman-collection)
    - [Environment file](#environment-file)
    - [REST API Authentication](#rest-api-authentication)
  - [Heroku Deployment](#heroku-deployment)
    - [Steps](#steps)

</br>

## Requirements

This list covers requirements for local development and deployment to Heroku (note that you are free to deploy this server on other platforms).

- [ ] [Python](https://www.python.org/) (*the version is declared in the `environment.yml` file*)
- [ ] [Anaconda](https://www.anaconda.com/) or some other Python environment manager (*optional but recommended*)
- [ ] Tableau Server or a Tableau Cloud site (a developer site is available for free by signing up for the [developer program](https://www.tableau.com/developer))
- [ ] Authentication to Tableau's REST API is performed either via `PAT` (*personal access token*) by default as well as username and password or `JWT` (*Connected Apps*). Refer to the documentation for [REST API authentication](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_authentication.htm#sign_in) for more information. **NOTE**: currently `JWT` authentication does not support all RESTful methods listed in the documentation.
- [ ] [Postman](https://www.postman.com/) to make test requests to the [Tableau Webhooks API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_webhooks.htm) or to test the automation server during local development (*optional*)
- [ ] [Request Bin](https://requestbin.com/) a useful and free service you can use to receive real webhooks requests for development (*optional*)

</br>

## Installation

1. Clone this repository
```bash
git clone git@github.com:stephenlprice/tableau-webhooks.git
# or
git clone https://github.com/stephenlprice/tableau-webhooks.git

# navigate to the project directory
cd tableau-webhooks
```
1. Create a `conda` environment to install all dependencies and activate it (*see [Dependencies](#dependencies) for more info*). To install `conda` on a new machine, refer to the [Anaconda website](https://www.anaconda.com/).
```bash
# will create an environment called tableau-webhooks
conda env create -f environment.yml

# activates the environment
conda activate tableau-webhooks

# lists existing conda environments
# adds an asterisk next to the active environment
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
# $(MODULE_NAME) is index and $(VARIABLE_NAME) is app 
# (index.py is where the Flask server is initialized)
gunicorn index:app
```

</br>

## Dependencies

This project was built with [Anaconda](https://www.anaconda.com/) to manage Python environments, therefore the development environment can be cloned from the `environment.yml` file. Most dependencies are installed with `conda` while the last two are installed with `pip3`.

Managing Python environments is a best practice and well described by the following [xkcd 1987](https://xkcd.com/1987/):

<p align="center">
<img src="assets/images/xkcd-1987.png" alt="xkcd 1987 comic">
</p>

<h6><i><strong>NOTE</strong>: Superfund sites are bad. Do yourself a favor and just get <code>conda</code>.</i></h6>

</br>

If you are new to `conda` I recommend keeping the [conda cheatsheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf) nearby for reference.

These are the contents of the `environment.yml` file:

```yaml
name: tableau-webhooks
channels:
  - defaults
dependencies:
  - python=3.9.12
  - flask=2.0.2
  - gunicorn=20.1.0
  - requests=2.28.1
  - pip=21.2.4
  - pip:
    - python-dotenv==0.19.2
    - pyjwt[crypto]==2.4.0
```

It is possible to recreate this environment without Anaconda, using something like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/). In that case you can install all dependencies with `pip3` and write a `requirements.txt` file to document your dependencies.

</br>

## Environment Variables

To protect private data such as PATs this project relies on `environment variables`, that way this information is available in development and production environments without pushing them to Git repositories (via `.gitignore`). If you are new to this concept I highly recommend that you read [Twilio's blog post](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html) on the subject. The `python-dotenv` package will load these variables into the server when initialized.

```bash
# create a .env file
touch .env
```

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
FLASK_ENV='default is production, set to development for debugging'
```
If you add integrations to other services such as Slack or Twilio, this would be the right place to store credentials needed to authenticate to 3rd parties.

If you only use one REST API authentication mechanism (*`PAT` for example*), you can provide empty strings for other values such as `TABLEAU_CA_CLIENT`, `TABLEAU_CA_SECRET_ID`, `TABLEAU_CA_SECRET_VALUE` that are used by `JWT` authentication.

</br>

## Local Usage

The app was built in [Python](https://www.python.org/) using the [Flask](https://palletsprojects.com/p/flask/) micro web framework. `Flask` can run on it's own for development purposes however, this is not recommended for production and instead a WSGI server such as [gunicorn](https://gunicorn.org/) is required.

To start the server with `gunicorn` you can run this command:

```bash
# $(MODULE_NAME) is index and $(VARIABLE_NAME) is app 
# (index.py is where the Flask server is initialized)
gunicorn index:app
```

As a result the server will be available at: 

```bash
http://127.0.0.1:8000
# the endpoint used for incoming webhooks
http://127.0.0.1:8000/webhook
```

For development purposes it is also acceptable to start the server this way:

```bash
# this should allow for live updates as you code
python index.py
```

You can simulate webhook behavior by sending requests with sample payloads described in the [Webhooks API](https://www.tableau.com/developer/tools/webhook-api) documentation:

```bash
curl "http://127.0.0.1:8000/webhook" \ 
-X POST \
-H "Content-Type: application/json" \
-d @filename
```

</br>

## Postman Collection

<p align="center">
<img src="assets/images/postman.png" alt="xkcd 1987 comic">
</p>

This repository contains a [Postman](https://www.postman.com/) collection and environment file to help you interact with [REST API endpoints](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_notifications.htm#create_webhook) used to configure Tableau webhooks.

Once you have added a webhook to a Tableau site, you can test it using the `test` request provided in the collection. It is also useful to get a `list` of webhooks registered on the server to get the ID of a webhook that you wish to test.

### Environment file

The Postman collection was built to leverage the provided environment file which will store useful information such as credentials and URLs as well as allowing scripts to update variables for you automatically.

> ##### *__WARNING__: Do not push usernames, passwords or personal access tokens to Github as they will be accessible by crawlers and is a well known security risk. You can fork environment files for local use and keep an empty template available on the repository for others to use.*
> 

</br>

Postman will also help you test the behavior you have written for each event type in `webhooks.py`. You can send `POST` requests to the `http://127.0.0.1:8000/webhook` URL and create test payloads obtained from the [Webhooks API documentation](https://www.tableau.com/developer/tools/webhook-api) or replace test values with real values from resources on your Tableau environment to observe how real workflows run.

</br>

### REST API Authentication

To send requests to Tableau's RESTful endpoints you will need to authenticate by way of a via `PAT` (*personal access token*), username & password or `JWT` (*Connected App*). Successful authentication will return an `API key` that is added to the `X-Tableau-Auth` header, allowing users to send requests to protected endpoints. 

Refer to the documentation for [REST API authentication](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_authentication.htm#sign_in) for more information. By default, the automation server will use a `PAT`.  **NOTE**: currently `JWT` authentication does not support all RESTful methods listed in the documentation.

</br>

## Heroku Deployment

![production deployment](assets/images/flask-gunicorn.png)
<h6><i><strong>Source</strong>: <a href="https://eserdk.medium.com/heroku-nginx-gunicorn-flask-f10e81aca90d" target="_blank">Medium: Configuring heroku-based nginx and gunicorn to serve static content and to pass requests directly to the app</a></i></h6>

</br>

The app is setup for deployment on [Heroku](https://heroku.com/). Deployment to this platform has a few requirements:

- [ ] [Heroku](https://heroku.com/) account
- [ ] Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [ ] An `environment.yml` or `requirements.txt` file
- [ ] A `Procfile` (instructions for starting your dyno)
- [ ] Heroku buildpacks for [conda](https://elements.heroku.com/buildpacks/pl31/heroku-buildpack-conda) or [python](https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-python) (will install project dependencies)

### Steps

1. Add a [Heroku remote](https://devcenter.heroku.com/articles/git#creating-a-heroku-remote) (track this git repo on a Heroku app)
```bash
# creates a new app (declare a name or it will be randomly named)
heroku create {your-app-name}

# add an existing Heroku remote to the git repo
heroku git:remote -a {your-app-name}

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

3. The existing `Procfile` runs the command to launch a "web" dyno on Heroku
```bash
web: gunicorn index:app
```

4. Projects using `conda` environments can use the provided `environment.yml` file, otherwise you will have to create a `requirements.txt` file to install [python dependencies on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#declare-app-dependencies)

5. Add all of the [environment variables](#environment-variables) listed in the `example-env` file to the Heroku app's settings under "config vars" (this is done on the website)

</br>

   
> ##### *__WARNING__: the server will have a `RuntimeError` if these environment variables are not accessible.*
> 
</br>

6. Deploy [code to Heroku](https://devcenter.heroku.com/articles/git#deploying-code) 
```bash
# pushes your git branch to the Heroku remote
git push heroku {branch-name}
```
