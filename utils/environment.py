from utils import exceptions


def validate(env_dict, env_vars):
  # check that each environment variable has been declared and assigned
  for vars in env_vars:
    try:
      # check the local dictionary pulled from os.environ
      env_dict[vars]

      # check that key value length is non-zero
      if len(env_dict[vars]) == 0:
        raise exceptions.EnvironmentAttributeError(vars)

    except KeyError as error:
      # raises error if an environment variable has not been declared
      raise exceptions.EnvironmentKeyError(vars, error)
