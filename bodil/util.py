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

def bits_to_quads(mask):
    """Converts cidr bits (24) to dotted quads (255.255.255.0).

    Args:
        mask (int): cidr bits

    Returns:
        str: Dotted quads

    Examples:
        >>> bits_to_quads(24)
        "255.255.255.0"
    """
    bits = 0
    for i in xrange(32-mask,32):
        bits |= (1 << i)
    return "%d.%d.%d.%d" % ((bits & 0xff000000) >> 24, (bits & 0xff0000) >> 16, (bits & 0xff00) >> 8 , (bits & 0xff))

