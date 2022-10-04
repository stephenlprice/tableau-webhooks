import json
from modules import broadcast
from utils import log, exceptions

# entry point to webhooks handling, determines which resource fired the webhook
def handleEvent(payload, env_dict):
  # verify that the webhook request is not a duplicate
  if duplicate(payload) == False:
    # request objects lacking these keys automatically raise a KeyError
    event_type = payload["event_type"]
    resource = payload["resource"]
    # ignore test requests (Flask will send an HTTP 202 response)
    if event_type == "Test":
      log.logger.debug("Test Request Received")
      return
    elif "workbook" in event_type.lower():
      workbook(payload, env_dict)
    elif "admin" in event_type.lower():
      datasource(payload, env_dict)
    elif "user" in event_type.lower():
      user(payload, env_dict)
    else:
      raise exceptions.WebhookEventTypeError(event_type)

    # commented out until resource enums are clarified in documentation
    # else:
    #   if resource == "WORKBOOK":
    #     workbook(payload, env_dict)
    #   elif resource == "DATASOURCE":
    #     datasource(payload, env_dict)
    #   elif resource == "USER":
    #     user(payload, env_dict)
    #   else:
    #     raise exceptions.WebhookEventResourceError(resource)
  else:
    # ignore if the webhook payload is a duplicate
    return


# handle duplicate payloads from the same Tableau event 
# (https://help.tableau.com/current/developer/webhooks/en-us/docs/webhooks-events-payload.html#tableau-webhooks-behavior)
def duplicate(payload):
  previous_payload = None
  if previous_payload != payload:
    # store the new payload for future duplicate filtering
    previous_payload = payload
    return False
  else:
    return True


# handle workbook events
def workbook(payload, env_dict):
  # request objects lacking these keys automatically raise a KeyError
  event_type = payload["event_type"]
  workbook_id = payload["resource_luid"]

  # handle different webhook event types
  if event_type == "WorkbookRefreshSucceeded":
    log.logger.debug("Workbook Refresh Succeeded: %s" % json.dumps(payload, indent=2, sort_keys=True))
    # determine if the workbook should update a broadcast
    broadcast.update(env_dict, workbook_id)

  elif event_type == "WorkbookRefreshFailed":
    log.logger.debug("Workbook Refresh Failed: %s" % json.dumps(payload, indent=2, sort_keys=True))

  elif event_type == "WorkbookRefreshStarted":
    log.logger.debug("Workbook Refresh Started: %s" % json.dumps(payload, indent=2, sort_keys=True))

  elif event_type == "WorkbookUpdated":
    log.logger.debug("Workbook Updated: %s" % json.dumps(payload, indent=2, sort_keys=True))
    # determine if the workbook should update a broadcast
    broadcast.update(env_dict, workbook_id)
  
  elif event_type == "WorkbookCreated":
    log.logger.debug("Workbook Created: %s" % json.dumps(payload, indent=2, sort_keys=True))
  
  elif event_type == "WorkbookDeleted":
    log.logger.debug("Workbook Deleted: %s" % json.dumps(payload, indent=2, sort_keys=True))

  # label events can fire for both workbook or datasource resources
  elif event_type == "LabelCreated":
    log.logger.debug("Label Created: %s" % json.dumps(payload, indent=2, sort_keys=True))
  
  elif event_type == "LabelUpdated":
    log.logger.debug("Label Updated: %s" % json.dumps(payload, indent=2, sort_keys=True))
  
  elif event_type == "LabelDeleted":
    log.logger.debug("Label Deleted: %s" % json.dumps(payload, indent=2, sort_keys=True))

  else:
    raise exceptions.WebhookEventTypeError(event_type)


# handle datasource events
def datasource(payload, env_dict):
  # request objects lacking these keys automatically raise a KeyError
  event_type = payload["event_type"]
  datasource_id = payload["resource_luid"]

  # handle different webhook event types
  if event_type == "DatasourceRefreshSucceeded":
    log.logger.debug("Datasource Refresh Succeeded: %s" % json.dumps(payload, indent=2, sort_keys=True))

  elif event_type == "DatasourceRefreshFailed":
    log.logger.debug("Datasource Refresh Failed: %s" % json.dumps(payload, indent=2, sort_keys=True))

  elif event_type == "DatasourceRefreshStarted":
    log.logger.debug("Datasource Refresh Started: %s" % json.dumps(payload, indent=2, sort_keys=True))

  elif event_type == "DatasourceUpdated":
    log.logger.debug("Datasource Updated: %s" % json.dumps(payload, indent=2, sort_keys=True))
  
  elif event_type == "DatasourceCreated":
    log.logger.debug("Datasource Created: %s" % json.dumps(payload, indent=2, sort_keys=True))
  
  elif event_type == "DatasourceDeleted":
    log.logger.debug("Datasource Deleted: %s" % json.dumps(payload, indent=2, sort_keys=True))

  # label events can fire for both workbook or datasource resources
  elif event_type == "LabelCreated":
    log.logger.debug("Label Created: %s" % json.dumps(payload, indent=2, sort_keys=True))
  
  elif event_type == "LabelUpdated":
    log.logger.debug("Label Updated: %s" % json.dumps(payload, indent=2, sort_keys=True))
  
  elif event_type == "LabelDeleted":
    log.logger.debug("Label Deleted: %s" % json.dumps(payload, indent=2, sort_keys=True))

  else:
    raise exceptions.WebhookEventTypeError(event_type)


# handle user events
def user(payload, env_dict):
  # request objects lacking these keys automatically raise a KeyError
  event_type = payload["event_type"]
  user_id = payload["resource_luid"]

  # handle different webhook event types
  if event_type == "AdminPromoted":
    log.logger.debug("Admin Promoted: %s" % json.dumps(payload, indent=2, sort_keys=True))

  elif event_type == "AdminDemoted":
    log.logger.debug("Admin Demoted: %s" % json.dumps(payload, indent=2, sort_keys=True))

  else:
    raise exceptions.WebhookEventTypeError(event_type)
