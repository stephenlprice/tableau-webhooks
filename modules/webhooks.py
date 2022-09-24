import json
from modules import broadcast
from utils import log, exceptions

def workbook(payload, env_dict):
  # request objects lacking these keys automatically raise a KeyError
  event_type = payload["event_type"]
  workbook_id = payload["resource_luid"]

  # handle different webhook event types
  if event_type == "WorkbookRefreshSucceeded":
    log.logger.info(f"Workbook Refresh Succeeded: {json.dumps(payload, indent=2, sort_keys=True)}")
    # determine if the workbook should update a broadcast
    broadcast.update(env_dict, workbook_id)

  elif event_type == "WorkbookRefreshFailed":
    log.logger.error(f"Workbook Refresh Failed: {json.dumps(payload, indent=2, sort_keys=True)}")

  elif event_type == "WorkbookUpdated":
    log.logger.info(f"Workbook Updated: {json.dumps(payload, indent=2, sort_keys=True)}")
    # determine if the workbook should update a broadcast
    broadcast.update(env_dict, workbook_id)

  elif event_type == "WorkbookDeleted":
    log.logger.info(f"Workbook Deleted: {json.dumps(payload, indent=2, sort_keys=True)}")

  else:
    raise exceptions.WebhookEventTypeError(event_type)
