import os
from dotenv import load_dotenv
from utils import log, environment
from modules import connected_apps, rest

# dictionary with required environment variables
env_vars = [
  "TABLEAU_SERVER",
  "TABLEAU_SITENAME",
  "TABLEAU_RESTAPI_VERSION",
  "TABLEAU_USERNAME",
  "TABLEAU_CA_CLIENT",
  "TABLEAU_CA_SECRET_ID",
  "TABLEAU_CA_SECRET_VALUE"
]

# load environment files from .env
load_dotenv("../.env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)

# validate environment variables
environment.validate(env_dict, env_vars)
print('SUCCESS: environment validation passed...')
log.logger.info('SUCCESS: environment validation passed...')

# encode a JWT token for connected apps authentication: https://help.tableau.com/current/online/en-us/connected_apps.htm#step-4-embedding-next-steps
jwt = connected_apps.encode(env_dict)
print('SUCCESS: jwt encoded...')
log.logger.info('SUCCESS: jwt encoded...')


# authenticate to Tableau's REST API
api_key = rest.auth(env_dict, jwt)
print('SUCCESS: REST API key obtained...')
log.logger.info('SUCCESS: REST API key obtained...')

# get a list of workbooks on the site
workbooks = rest.get_workbooks_site(api_key)
print('SUCCESS: Workbooks queried...')
log.logger.info('SUCCESS: Workbooks by site queried...')
