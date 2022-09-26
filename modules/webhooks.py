import json
from modules import broadcast
from utils import log, exceptions

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
  if duplicate(payload) == False:
    # request objects lacking these keys automatically raise a KeyError
    event_type = payload["event_type"]
    workbook_id = payload["resource_luid"]

    # handle different webhook event types
    if event_type == "WorkbookRefreshSucceeded":
      log.logger.info(f"Workbook Refresh Succeeded: {0}".format(json.dumps(payload, indent=2, sort_keys=True)))
      # determine if the workbook should update a broadcast
      broadcast.update(env_dict, workbook_id)

    elif event_type == "WorkbookRefreshFailed":
      log.logger.error(f"Workbook Refresh Failed: {0}".format(json.dumps(payload, indent=2, sort_keys=True)))

    elif event_type == "WorkbookUpdated":
      log.logger.info(f"Workbook Updated: {0}".format(json.dumps(payload, indent=2, sort_keys=True)))
      # determine if the workbook should update a broadcast
      broadcast.update(env_dict, workbook_id)

    else:
      raise exceptions.WebhookEventTypeError(event_type)

  else:
    # ignore if the webhook payload is a duplicate
    pass
