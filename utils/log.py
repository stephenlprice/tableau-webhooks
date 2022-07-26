import logging

# instantiate a logger object writing to connected-apps.log
logging.basicConfig(
  format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
  datefmt='%Y-%m-%d:%H:%M:%S',
  level=logging.DEBUG,
  filename='logs/webhooks.log'
)    
# logger object named after module: https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial
logger = logging.getLogger(__name__)
