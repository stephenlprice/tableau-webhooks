from libs import connected_apps, tableau_rest

def update(env_dict, workbook_id):
  # authenticate to Tableau's REST API
  api_key = tableau_rest.auth_pat(env_dict)

  # get all broadcasts on the site
  broadcasts = tableau_rest.get_broadcasts(api_key)

  # update the broadcast
  tableau_rest.update_broadcast(api_key, broadcasts, workbook_id, False, False)
  