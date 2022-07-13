import os, datetime, uuid
from dotenv import load_dotenv
import jwt

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
