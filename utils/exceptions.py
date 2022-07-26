from utils import log

class Error(Exception):
  """base class for errors"""


class EnvironmentAttributeError(Error):
  """
  Exception raised when environment variables are empty strings

  Attributes:
    key_attribute -- environment variable
  """

  def __init__(self, environment_variable):
    self.environment_variable = environment_variable
    self.message = f"Environment variable value for key {environment_variable} was not assigned."
    self.log = log.logger.error(f"Environment variable value for key {environment_variable} was not assigned.")
    super().__init__(self.message)


class EnvironmentKeyError(Error):
  """
  Exception raised when the environment variables dict does not have required keys

  Attributes:
    key_attribute -- environment variable
  """

  def __init__(self, vars):
    self.environment_variable = vars
    self.message = f"Environment variable {vars} was not declared."
    self.log = log.logger.error(f"Environment variable {vars} was not declared.")
    super().__init__(self.message)


class JWTEncodingError(Error):
  """
  Exception raised when encoding fails

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = f"Cannot encode JWT: {error}"
    self.log = log.logger.error(f"Cannot encode JWT: {error}")
    super().__init__(self.message)


class JWTDecodingError(Error):
  """
  Exception raised when decoding fails

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = f"Cannot decode JWT: {error}"
    self.log = log.logger.error(f"Cannot decode JWT: {error}")
    super().__init__(self.message)


class TableauRestAuthError(Error):
  """
  Exception raised when authentication to Tableau's REST API fails

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = f"Authentication to Tableau REST API failed: {error}"
    self.log = log.logger.error(f"Authentication to Tableau REST API failed: {error}")
    super().__init__(self.message)


class TableauRestError(Error):
  """
  Exception raised when requests to Tableau's REST API fail

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = f"Request to Tableau REST API failed: {error}"
    self.log = log.logger.error(f"Request to Tableau REST API failed: {error}")
    super().__init__(self.message)


class TableauGetBroadcast(Error):
  """
  Exception raised when get_broadcast requests to Tableau's REST API fail

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = f"Get Broadcast failed: {error}"
    self.log = log.logger.error(f"Get Broadcast failed: {error}")
    super().__init__(self.message)


class TableauUpdateBroadcast(Error):
  """
  Exception raised when update_broadcast requests to Tableau's REST API fail

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = f"Update Broadcast failed: {error}"
    self.log = log.logger.error(f"Update Broadcast failed: {error}")
    super().__init__(self.message)
    