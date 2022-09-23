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
  def __init__(self, tableau_domain, site_name, api_version, session_minutes):
    self.paths.classic = f"{tableau_domain}/api/{api_version}"
    self.paths.new = f"{tableau_domain}/api/exp"
    self.site_name = site_name
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
