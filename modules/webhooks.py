import json
from modules import broadcast
from utils import log, exceptions

# entry point to webhooks handling, determines which resource fired the webhook
def handleEvent(payload, env_dict):
  # verify that the webhook request is not a duplicate
  if handle_duplicate(payload) == False:
    # request objects lacking these keys automatically raise a KeyError
    event_type = payload["event_type"]
    resource = payload["resource"]

    # output event details for debugging in development environment
    debug_event(payload)

    # ignore test requests (Flask will send an HTTP 202 response)
    if event_type == "Test":
      log.logger.debug("Test Request Received")
      return
    elif "workbook" in event_type.lower():
      workbook(payload, env_dict)
    elif "datasource" in event_type.lower():
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
def handle_duplicate(payload):
  previous_payload = None
  if previous_payload != payload:
    # store the new payload for future duplicate filtering
    previous_payload = payload
    return False
  else:
    return True

# outputs webhook events to stderr to debug behavior
def debug_event(payload):
  log.logger.debug("%(event_type)s: %(payload)s" % {
    "event_type": payload["event_type"],
    "payload": json.dumps(payload, indent=2, sort_keys=True)
    }
  )


# handle workbook events
def workbook(payload, env_dict):
  # request objects lacking these keys automatically raise a KeyError
  event_type = payload["event_type"]
  workbook_id = payload["resource_luid"]

  # handle different webhook event types
  if event_type == "WorkbookRefreshSucceeded":
    # determine if the workbook should update a broadcast
    broadcast.update(env_dict, workbook_id)

  elif event_type == "WorkbookRefreshFailed":
    pass

  elif event_type == "WorkbookRefreshStarted":
    pass

  elif event_type == "WorkbookUpdated":
    # determine if the workbook should update a broadcast
    broadcast.update(env_dict, workbook_id)
  
  elif event_type == "WorkbookCreated":
    pass
  
  elif event_type == "WorkbookDeleted":
    pass

  # label events can fire for both workbook or datasource resources
  elif event_type == "LabelCreated":
    pass
  
  elif event_type == "LabelUpdated":
    pass
  
  elif event_type == "LabelDeleted":
    pass

  else:
    raise exceptions.WebhookEventTypeError(event_type)


# handle datasource events
def datasource(payload, env_dict):
  # request objects lacking these keys automatically raise a KeyError
  event_type = payload["event_type"]
  datasource_id = payload["resource_luid"]

  # handle different webhook event types
  if event_type == "DatasourceRefreshSucceeded":
    pass

  elif event_type == "DatasourceRefreshFailed":
    pass

  elif event_type == "DatasourceRefreshStarted":
    pass

  elif event_type == "DatasourceUpdated":
    pass
  
  elif event_type == "DatasourceCreated":
    pass
  
  elif event_type == "DatasourceDeleted":
    pass

  # label events can fire for both workbook or datasource resources
  elif event_type == "LabelCreated":
    pass
  
  elif event_type == "LabelUpdated":
    pass
  
  elif event_type == "LabelDeleted":
    pass

  else:
    raise exceptions.WebhookEventTypeError(event_type)


# handle user events
def user(payload, env_dict):
  # request objects lacking these keys automatically raise a KeyError
  event_type = payload["event_type"]
  user_id = payload["resource_luid"]

  # handle different webhook event types
  if event_type == "AdminPromoted":
    pass

  elif event_type == "AdminDemoted":
    pass

  else:
    raise exceptions.WebhookEventTypeError(event_type)
