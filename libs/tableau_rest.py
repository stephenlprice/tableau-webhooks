import requests
import json
from utils import exceptions, log

credentials = {
  "site_id": "",
  "api_key": ""
}

paths = {
  "classic": "",
  "new": "",
}

# authentication into tableau's REST API with a valid JWT
def auth_jwt(env_dict, jwt):
  # assign environment variables to built paths for classic and new resources https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_versions.htm
  paths['classic'] = f"{env_dict['TABLEAU_SERVER']}/api/{env_dict['TABLEAU_RESTAPI_VERSION']}"
  paths['new'] = f"{env_dict['TABLEAU_SERVER']}/api/exp"
  # the path used for authentication
  auth_url = f'{paths["classic"]}/auth/signin'

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
    response = requests.request("POST", auth_url, headers=auth_headers, data=auth_payload.format(jwt, env_dict["TABLEAU_SITENAME"]))

  except Exception as error:
    raise exceptions.TableauRestAuthError(error)

  else:
    response_body = response.json()
    log.logger.info(f"Successful authentication to Tableau REST API: {json.dumps(response_body, indent=2, sort_keys=True)}")
    print(f"Successful authentication to Tableau REST API: {json.dumps(response_body, indent=2, sort_keys=True)}")

    # assign credential and path values from response
    credentials["site_id"] = response_body["credentials"]["site"]["id"]
    credentials["api_key"] = response_body["credentials"]["token"]

    # successful JWT authentication returns an API key to be used in future requests
    return credentials["api_key"]


# authentication into tableau's REST API with a valid PAT
def auth_pat(env_dict):
  # assign environment variables to built paths for classic and new resources https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_versions.htm
  paths['classic'] = f"{env_dict['TABLEAU_SERVER']}/api/{env_dict['TABLEAU_RESTAPI_VERSION']}"
  paths['new'] = f"{env_dict['TABLEAU_SERVER']}/api/exp"
  # the path used for authentication
  auth_url = f'{paths["classic"]}/auth/signin'

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
    print(f"Successful authentication to Tableau REST API: {json.dumps(response_body, indent=2, sort_keys=True)}")

    # assign credential and path values from response
    credentials["site_id"] = response_body["credentials"]["site"]["id"]
    credentials["api_key"] = response_body["credentials"]["token"]

    # successful JWT authentication returns an API key to be used in future requests
    return credentials["api_key"]


# get all views on the site
def get_views_site(api_key):
  views_url = f'{paths["new"]}/sites/{credentials["site_id"]}/views'

  payload={}
  headers = {
    'Accept': 'application/json',
    'X-Tableau-Auth': api_key
  }

  try:
    response = requests.request("GET", views_url, headers=headers, data=payload)

  except Exception as error:
    raise exceptions.TableauRestError(error)

  else:
    response_body = response.json()
    log.logger.info(f"Views on site: {json.dumps(response_body, indent=2, sort_keys=True)}")
    print(f"Views on site: {json.dumps(response_body, indent=2, sort_keys=True)}")
    
    # successful request returns a list of views with workbook ids
    return response_body


# get a list of broadcast views
def get_broadcasts(api_key):
  broadcasts_url = f'{paths["new"]}/sites/{credentials["site_id"]}/broadcasts/views'

  payload={}
  headers = {
    'Accept': 'application/json',
    'X-Tableau-Auth': api_key,
  }

  try:
    response = requests.request("GET", broadcasts_url, headers=headers, data=payload)

  except Exception as error:
    raise exceptions.TableauGetBroadcast(error)
  
  else:
    response_body = response.json()
    log.logger.info(f"Broadcasts on site: {json.dumps(response_body, indent=2, sort_keys=True)}")
    print(f"Broadcasts on site: {json.dumps(response_body, indent=2, sort_keys=True)}")

    return response_body


# update the broadcast
def update_broadcast(api_key, broadcasts, workbook_id, show_watermark, show_tabs):
  params = '?acceptTermsOfUse=true&overwrite=yes'
  update_url = f'{paths["new"]}/sites/{credentials["site_id"]}/broadcasts/views{params}'

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
        'X-Tableau-Auth': api_key,
        'Content-Type': 'application/json',
      }
      
      try:
        response = requests.request("POST", update_url, headers=headers, data=payload)
      
      except Exception as error:
        raise exceptions.TableauUpdateBroadcast(error)
      
      else:
        response_body = response.json()
        log.logger.info(f"Broadcast updated: {json.dumps(response_body, indent=2, sort_keys=True)}")
        print(f"Broadcast updated: {json.dumps(response_body, indent=2, sort_keys=True)}")
