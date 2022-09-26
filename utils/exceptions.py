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
    self.message = "Environment variable value for key %s was not assigned." % environment_variable
    self.log = log.logger.error("Environment variable value for key %s was not assigned." % environment_variable)
    super().__init__(self.message)


class EnvironmentKeyError(Error):
  """
  Exception raised when the environment variables dict does not have required keys

  Attributes:
    key_attribute -- environment variable
  """

  def __init__(self, vars):
    self.environment_variable = vars
    self.message = "Environment variable %s was not declared." % vars
    self.log = log.logger.error("Environment variable %s was not declared." % vars)
    super().__init__(self.message)


class JWTEncodingError(Error):
  """
  Exception raised when encoding fails

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = "Cannot encode JWT: %s" % error
    self.log = log.logger.error("Cannot encode JWT: %s" % error)
    super().__init__(self.message)


class JWTDecodingError(Error):
  """
  Exception raised when decoding fails

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = "Cannot decode JWT: %s" % error
    self.log = log.logger.error("Cannot decode JWT: %s" % error)
    super().__init__(self.message)


class WebhookEventResourceError(Error):
  """
  Exception raised when a webhook resource is unexpected

  Attributes:
    key_attribute -- resource
  """

  def __init__(self, resource):
    self.message = "Unexpected Webhook Resource: %s" % resource
    self.log = log.logger.error("Unexpected Webhook Resource: %s" % resource)
    super().__init__(self.message)


class WebhookEventTypeError(Error):
  """
  Exception raised when a webhook event type is unexpected

  Attributes:
    key_attribute -- event_type
  """

  def __init__(self, eventType):
    self.message = "Unexpected Webhook Event: %s" % eventType
    self.log = log.logger.error("Unexpected Webhook Event: %s" % eventType)
    super().__init__(self.message)


class TableauRestAuthError(Error):
  """
  Exception raised when authentication to Tableau's REST API fails

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = "Authentication to Tableau REST API failed: %s" % error
    self.log = log.logger.error("Authentication to Tableau REST API failed: %s" % error)
    super().__init__(self.message)


class TableauRestError(Error):
  """
  Exception raised when requests to Tableau's REST API fail

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = "Request to Tableau REST API failed: %s" % error
    self.log = log.logger.error("Request to Tableau REST API failed: %s" % error)
    super().__init__(self.message)


class TableauRestGetBroadcast(Error):
  """
  Exception raised when get_broadcast requests to Tableau's REST API fail

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = "Get Broadcast failed: %s" % error
    self.log = log.logger.error("Get Broadcast failed: %s" % error)
    super().__init__(self.message)


class TableauRestUpdateBroadcast(Error):
  """
  Exception raised when update_broadcast requests to Tableau's REST API fail

  Attributes:
    key_attribute -- error
  """

  def __init__(self, error):
    self.message = "Update Broadcast failed: %s" % error
    self.log = log.logger.error("Update Broadcast failed: %s" % error)
    super().__init__(self.message)

    