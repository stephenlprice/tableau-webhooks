from utils import log
from libs import connected_apps, tableau_rest

def update(env_dict):
  # encode a JWT token for connected apps authentication: https://help.tableau.com/current/online/en-us/connected_apps.htm#step-4-embedding-next-steps
  jwt = connected_apps.encode(env_dict)
  print('SUCCESS: jwt encoded...')
  log.logger.info('SUCCESS: jwt encoded...')

  # authenticate to Tableau's REST API
  api_key = tableau_rest.auth(env_dict, jwt)
  print('SUCCESS: REST API key obtained...')
  log.logger.info('SUCCESS: REST API key obtained...')

  # get a list of workbooks on the site
  workbooks = tableau_rest.get_workbooks_site(api_key)
  print('SUCCESS: Workbooks queried...')
  log.logger.info('SUCCESS: Workbooks by site queried...')