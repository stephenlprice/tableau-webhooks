import requests
import json
from tableau_session import TableauEnv
from utils import exceptions, log


# authentication into tableau's REST API with a valid JWT
def auth_jwt(env_dict, jwt):
  # pass environment variables to create an object used to establish a session with a Tableau site
  tableau_session = TableauEnv(env_dict, 'jwt')

  # the path used for authentication
  auth_url = f'{tableau_session.paths.classic}/auth/signin'

  auth_payload = """
  <tsRequest>
    <credentials jwt="{0}">
      <site contentUrl="{1}"/>
    </credentials>
  </tsRequest>
  """

  auth_headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/json'
  }

  try:
    response = requests.request("POST", auth_url, headers=auth_headers, data=auth_payload.format(jwt, tableau_session.site_name))

  except Exception as error:
    raise exceptions.TableauRestAuthError(error)

  else:
    response_body = response.json()
    log.logger.info(f"Successful authentication to Tableau REST API: {json.dumps(response_body, indent=2, sort_keys=True)}")

    # assign id and api key values from response
    tableau_session.site_id = response_body["credentials"]["site"]["id"]
    tableau_session.api_key = response_body["credentials"]["token"]

    # JWT authentication returns a tableau_session object to be used in subsequent requests
    return tableau_session


# authentication into tableau's REST API with a valid PAT
def auth_pat(env_dict):
  # pass environment variables to create an object used to establish a session with a Tableau site
  tableau_session = TableauEnv(env_dict, 'pat')

  # the path used for authentication
  auth_url = f'{tableau_session.paths.classic}/auth/signin'

  auth_payload = """
  <tsRequest>
    <credentials personalAccessTokenName="{0}" personalAccessTokenSecret="{1}">
        <site contentUrl="{2}"/>
    </credentials>
  </tsRequest>
  """

  auth_headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/json'
  }

  try:
    response = requests.request("POST", auth_url, headers=auth_headers, data=auth_payload.format(env_dict["TABLEAU_PAT_NAME"], env_dict["TABLEAU_PAT_SECRET"], env_dict["TABLEAU_SITENAME"]))

  except Exception as error:
    raise exceptions.TableauRestAuthError(error)

  else:
    response_body = response.json()
    log.logger.info(f"Successful authentication to Tableau REST API: {json.dumps(response_body, indent=2, sort_keys=True)}")

    # assign id and api key values from response
    tableau_session.site_id = response_body["credentials"]["site"]["id"]
    tableau_session.api_key = response_body["credentials"]["token"]

    # JWT authentication returns a tableau_session object to be used in subsequent requests
    return tableau_session


# get all views on the site
def get_views_site(tableau_session):
  views_url = f'{tableau_session.paths.classic}/sites/{tableau_session.site_id}/views'


  payload={}
  headers = {
    'Accept': 'application/json',
    'X-Tableau-Auth': tableau_session.api_key
  }

  try:
    response = requests.request("GET", views_url, headers=headers, data=payload)

  except Exception as error:
    raise exceptions.TableauRestError(error)

  else:
    response_body = response.json()
    log.logger.info(f"Views on site: {json.dumps(response_body, indent=2, sort_keys=True)}")
    
    # successful request returns a list of views with workbook ids
    return response_body


# get a list of broadcast views
def get_broadcasts(tableau_session):
  broadcasts_url = f'{tableau_session.paths.new}/sites/{tableau_session.site_id}/broadcasts/views'

  payload={}
  headers = {
    'Accept': 'application/json',
    'X-Tableau-Auth': tableau_session.api_key,
  }

  try:
    response = requests.request("GET", broadcasts_url, headers=headers, data=payload)

  except Exception as error:
    raise exceptions.TableauRestGetBroadcast(error)
  
  else:
    response_body = response.json()
    log.logger.info(f"Broadcasts on site: {json.dumps(response_body, indent=2, sort_keys=True)}")

    # successful request returns a list of broadcast views with workbook ids
    return response_body


# update the broadcast
def update_broadcast(tableau_session, broadcasts, workbook_id, show_watermark, show_tabs):
  params = '?acceptTermsOfUse=true&overwrite=yes'
  update_url = f'{tableau_session.new}/sites/{tableau_session.site_id}/broadcasts/views{params}'

  # get all current broadcast views
  for broadcast in broadcasts['broadcastViews']['broadcast']:
    if broadcast['view']['workbook']['id'] == workbook_id:
      payload = json.dumps({
        "broadcastViewSend": {
          "viewId": broadcast['view']['id'],
          "showWatermark": show_watermark,
          "showTabs": show_tabs
        }
      })
      headers = {
        'Accept': 'application/json',
        'X-Tableau-Auth': tableau_session.api_key,
        'Content-Type': 'application/json',
      }

      try:
        response = requests.request("POST", update_url, headers=headers, data=payload)
      
      except Exception as error:
        raise exceptions.TableauRestPostBroadcast(error)
      
      else:
        response_body = response.json()
        log.logger.info(f"Broadcast updated: {json.dumps(response_body, indent=2, sort_keys=True)}")
