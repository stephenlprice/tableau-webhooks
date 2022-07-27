import logging
import sys

# logger object named after module: https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
  '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s', 
  datefmt='%Y-%m-%d:%H:%M:%S'
)

# create stream handler and set level to debug
sh = logging.StreamHandler(stream=sys.stdout)
sh.setLevel(logging.DEBUG)
# add formatter to sh
sh.setFormatter(formatter)
# create file handler
fh = logging.FileHandler(filename='logs/webhooks.log')
fh.setLevel(logging.DEBUG)
# add formatter to fh
fh.setFormatter(formatter)
# add sh & fh to logger
logger.addHandler(sh)
logger.addHandler(fh)
