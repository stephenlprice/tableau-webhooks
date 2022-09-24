from libs import tableau_rest
from utils import log

def update(env_dict, workbook_id):
  try:
    # authenticate to Tableau's REST API and establish a session
    tableau_session = tableau_rest.auth_pat(env_dict)

    # get all broadcasts on the site
    broadcasts = tableau_rest.get_broadcasts(tableau_session)

    # update the broadcast
    tableau_rest.update_broadcast(tableau_session, broadcasts, workbook_id, False, False)

  except Exception as error:
    log.logger.error("Cannot update Broadcast: ", error)

  else:
    log.logger.info("Broadcast update successful")
