""" This module defines the request manager for the APIs. """

from datetime import datetime

def get_request_id():
    """ get unique id for a particular request """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return timestamp
