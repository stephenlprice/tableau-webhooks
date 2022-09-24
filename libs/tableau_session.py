import tableau_rest
from utils import exceptions

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
  def __init__(self, tableau_domain, site_name, api_version, session_minutes, session_type):
    self.paths.classic = f"{tableau_domain}/api/{api_version}"
    self.paths.new = f"{tableau_domain}/api/exp"
    self.site_name = site_name
    self.session_type = session_type
    self.session_minutes = session_minutes
    self.session_date = None
    self.site_id = None
    self.api_key = None
    
  
  # string representation of the object
  def __str__(self):
    str = """
    Tableau Session for the site {0},
      ID: {1}
      Domain: {2}
      Started: {3}
      Duration: {4} minutes
    """

    return str.format(
      self.site_name, 
      self.site_id, 
      self.tableau_domain, 
      self.session_date, 
      self.session_minutes
    )
  
  # establishes a new session after timeout
  def new_session(self):
    if self.session_type == 'jwt':
      tableau_rest.auth_jwt
    elif self.session_type == 'pat':
      tableau_rest.auth_pat
    elif self.session_type == 'password':
      pass
    
