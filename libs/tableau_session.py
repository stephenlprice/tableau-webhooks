class TableauEnv:
  """
  Defines properties needed for REST API requests to a 
  given Tableau site. The object is first initialized with
  properties pointing to a Tableau domain and REST API version
  that are known before REST API authentication. After successful 
  authentication, other properties such as site id and api key 
  are set from the response payload.
  """
  def __init__(self, tableau_domain, site_name, api_version):
    self.paths.classic = f"{tableau_domain}/api/{api_version}"
    self.paths.new = f"{tableau_domain}/api/exp"
    self.name = site_name
    self.id = None
    self.api_key = None
  
  def __str__(self):
    return f"Tableau Session for the site {self.site_name} (ID: {self.site_id}), at {self.tableau_domain}"
