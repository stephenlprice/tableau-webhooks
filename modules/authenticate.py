from libs import connected_apps

def request(payload, env_dict):
  if payload['type'] == 'jwt':
    jwt = connected_apps.encode(payload, env_dict)

  elif payload['type'] == 'pat':
    pass

  elif payload['type'] == 'password':
    pass

  else:
    pass
