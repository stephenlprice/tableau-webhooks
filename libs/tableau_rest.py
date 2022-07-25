import requests
import json
from utils import exceptions, log

credentials = {
  "server": "",
  "api_version": "",
  "site_id": "",
  "api_key": ""
}

paths = {
  "classic": "",
  "new": "",
  "site": "",
}

# authentication into tableau's REST API with a valid JWT
def auth(env_dict, jwt):

  credentials['server'] = env_dict['TABLEAU_SERVER']
  credentials['api_version'] = env_dict['TABLEAU_RESTAPI_VERSION']
  paths['classic'] = f"{credentials['server']}/api/{credentials['api_version']}"
  paths['new'] = f"{credentials['server']}/api/exp"

  print('classic', paths["classic"])
  print('server', credentials["server"])

  auth_url = f'{paths["classic"]}/auth/signin'

  print('auth_url: ', auth_url)

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
  print(jwt)
  print(auth_payload.format(jwt, env_dict["TABLEAU_SITENAME"]))

  try:
    response = requests.request("POST", auth_url, headers=auth_headers, data=auth_payload.format(jwt, env_dict["TABLEAU_SITENAME"]))

  except Exception as error:
    raise exceptions.TableauRestAuthError(error)

  else:
    response_body = response.json()
    log.logger.info(f"Successful authentication to Tableau REST API: {json.dumps(response_body, indent=4, sort_keys=True)}")
    print(f"Successful authentication to Tableau REST API: {json.dumps(response_body, indent=4, sort_keys=True)}")

    # obtain dict values from response
    credentials["site_id"] = response_body["credentials"]["site"]["id"]
    credentials["api_key"] = response_body["credentials"]["token"]
    paths['site'] = f"sites/{credentials['site_id']}/"

    return credentials["api_key"]


# get a list of views for a site
def get_workbooks_site(api_key):
  
  query_parameters = f'pageSize=1&fields=_all_'

  workbooks_url = f'{paths["classic"]}/{paths["site"]}workbooks?{query_parameters}'

  print('workbooks_url: ', workbooks_url)

  payload={}
  headers = {
    'Accept': 'application/json',
    'X-Tableau-Auth': api_key
  }

  try:
    response = requests.request("GET", workbooks_url, headers=headers, data=payload)

  except Exception as error:
    raise exceptions.TableauRestError(error)
  
  else:
    response_body = response.json()
    log.logger.info(f"Successful request to Tableau REST API: {json.dumps(response_body, indent=4, sort_keys=True)}")
    print(f"Successful request to Tableau REST API: {json.dumps(response_body, indent=4, sort_keys=True)}")
