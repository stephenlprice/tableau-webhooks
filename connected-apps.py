import os, datetime, uuid
from dotenv import load_dotenv
import jwt
import requests

# load environment files from .env
load_dotenv("./.env")
# calling environ is expensive, this saves environment variables to a dictionary
env_dict = dict(os.environ)
# dictionary with required environment variables
env_vars = [
  "TABLEAU_USERNAME",
  "TABLEAU_CA_CLIENT",
  "TABLEAU_CA_SECRET_ID",
  "TABLEAU_CA_SECRET_VALUE", 
  "TABLEAU_SITENAME", 
  "TABLEAU_SERVER",
]

# check that each environment variable is available, else throw an exception
for vars in env_vars:
  try:
    # check the local dictionary pulled from os.environ
    env_dict[vars]
  except KeyError:
    # output the first environment variable to fail and shut the server down
    raise RuntimeError(f"Environment variable {vars} is not available, server shutting down...")

# tableau connected app variables (JWT) see: https://help.tableau.com/current/online/en-us/connected_apps.htm#step-3-configure-the-jwt
header_data = {
  "iss": env_dict["TABLEAU_CA_CLIENT"],
  "kid": env_dict["TABLEAU_CA_SECRET_ID"],
  "alg": "HS256",
}

payload_data = {
  "iss": env_dict["TABLEAU_CA_CLIENT"],
  "sub": env_dict["TABLEAU_USERNAME"],
  "aud": "tableau",
  "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
  "jti": str(uuid.uuid4()),
  "scp": ["tableau:content:read", "tableau:workbooks:create"]
}

connected_app_secret = env_dict["TABLEAU_CA_SECRET_VALUE"]

# encode the JWT with declared payload, secret and headers
token = jwt.encode(
  payload = payload_data,
  key = connected_app_secret,
  headers = header_data
)
print(f'encoded token: {token}')

# decode the JWT for testing purposes
decodedToken = jwt.decode(
  jwt = token, 
  key = connected_app_secret,
  audience = payload_data["aud"], 
  algorithms = header_data["alg"]
)
print(f'decoded token: {decodedToken}')


# authentication into tableau's REST API
base_path = f'{env_dict["TABLEAU_SERVER"]}/api'

auth_url = f'{base_path}/3.16/auth/signin'

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

print(auth_url)

print(auth_payload.format(token, env_dict["TABLEAU_SITENAME"]))

response = requests.request("POST", auth_url, headers=auth_headers, data=auth_payload.format(token, env_dict["TABLEAU_SITENAME"]))

response_body = response.json()
print(response_body)

# obtain dict values from response
site_id = response_body["credentials"]["site"]["id"]
api_key = response_body["credentials"]["token"]
print(site_id)

# get a list of views for a site
views_url = f'{base_path}/exp/sites/{site_id}/views'

payload={}
headers = {
  'Accept': 'application/json',
  'X-Tableau-Auth': api_key
}

response = requests.request("GET", views_url, headers=headers, data=payload)

print(response.text)

