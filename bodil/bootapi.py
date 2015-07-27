from flask import render_template
from flask.ext.restful import Resource

import bodil
from .machine import get_machine
from .util import abort_if_invalid_mac_address, plaintext_response


class BootAPI(Resource):
    def get(self, mac):
        abort_if_invalid_mac_address(mac)
        machine = get_machine(mac)

        template = 'boot-{}.ipxe'.format(machine.profile)
        res = plaintext_response(render_template(
            template, base_url=bodil.BODIL_URL,
            coreos_channel=machine.coreos_channel,
            coreos_version=machine.coreos_version))
        return res
