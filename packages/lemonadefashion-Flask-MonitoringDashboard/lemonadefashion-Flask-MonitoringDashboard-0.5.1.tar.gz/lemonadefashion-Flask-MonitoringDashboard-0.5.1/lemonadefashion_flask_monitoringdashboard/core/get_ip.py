from flask import request

from lemonadefashion_flask_monitoringdashboard import config
from lemonadefashion_flask_monitoringdashboard.core.logger import log

def get_ip():
    """
    :return: the ip address associated with the current request context
    """
    if config.get_ip:
        try:
            return config.get_ip()
        except Exception as e:
            log('Failed to execute provided get_ip function: {}'.format(e))
    # This is a reasonable fallback, but will not work for clients behind proxies.
    return request.environ['REMOTE_ADDR']
