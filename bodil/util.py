import re

from flask import make_response
from flask.ext.restful import abort


def plaintext_response(resp):
    res = make_response(resp)
    res.headers['Content-Type'] = 'text/plain'
    return res


def is_valid_mac_address(mac):
    """Validates the format of a MAC address.

    Args:
        mac (str): the MAC address to validate

    Returns:
        bool: True if valid, False otherwise

    Examples:
        >>> valid_mac('invalid_mac')
        False

        >>> valid_mac('28:cf:e9:18:ca:01')
        True
    """
    regex = "[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$"

    return re.match(regex, mac.lower())


def abort_if_invalid_mac_address(mac):
    """Abort request if given MAC address is invalid.

    Args:
        mac (str): the MAC address to test
    """
    if not is_valid_mac_address(mac):
        abort(400, message="Invalid MAC address: {}".format(mac))
