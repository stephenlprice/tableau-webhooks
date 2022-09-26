from libs import tableau_rest
from libs import connected_apps

class TableauEnv:
  """
  Defines properties needed for REST API requests to a 
  given Tableau site. The object is first initialized with
  properties pointing to a Tableau domain and REST API version
  that are known before REST API authentication. After successful 
  authentication, other properties such as site id and api key 
  are set from the response payload.
  """

  # assign values to properties on initialization and other operations
  def __init__(self, env_dict, session_type):    
    self.site_name = env_dict['TABLEAU_SITENAME']
    self.api_version = env_dict['TABLEAU_RESTAPI_VERSION']
    self.paths.classic = f"{env_dict['TABLEAU_DOMAIN']}/api/{self.api_version}"
    self.paths.new = f"{env_dict['TABLEAU_DOMAIN']}/api/exp"
    self.session_type = session_type
    self.session_minutes = env_dict['TABLEAU_SESSION_MINUTES']
    self.session_date = None
    self.site_id = None
    self.api_key = None
    
  # string representation of the object
  def __str__(self):
    message = """
    Tableau Session for the site {0},
      ID: {1}
      REST API version: {2}
      Domain: {3}
      Started: {4}
      Duration: {5} minutes
    """

    return message.format(
      self.site_name, 
      self.site_id, 
      self.api_version,
      self.tableau_domain, 
      self.session_date, 
      self.session_minutes
    )
  
  # establishes a new session after timeout
  def new_session(self, env_dict):
    if self.session_type == 'jwt':
      jwt = connected_apps.encode(env_dict)
      tableau_rest.auth_jwt(env_dict, jwt)
    elif self.session_type == 'pat':
      tableau_rest.auth_pat(env_dict)
    elif self.session_type == 'password':
      pass
