import logging
from .aliases import LOGGING_DIR


def create_and_updatelog(*args):
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG, 
    format='%(asctime)s %(levelname)-8s %(message)s', 
    datefmt='%a, %d %b %Y %H:%M:%S', 
    filename=LOGGING_DIR+'/log.log', 
    filemode='w')      
    logger.error(args)
