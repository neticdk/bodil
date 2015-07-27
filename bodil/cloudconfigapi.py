from flask import render_template
from flask.ext.restful import Resource

import bodil
from .machine import get_machine
from .util import abort_if_invalid_mac_address, plaintext_response


class CloudConfigAPI(Resource):
    def get(self, mac):
        abort_if_invalid_mac_address(mac)
        machine = get_machine(mac)

        template_fields = dict(base_url=bodil.BODIL_URL, ip=machine.ip,
                               gw=machine.gw, dns=machine.dns,
                               name=machine.name, sshkey=machine.sshkey,
                               etcd_token=machine.etcd_token)

        template = 'cloud-config-{}.yml'.format(machine.profile)
        res = plaintext_response(render_template(template, **template_fields))
        return res
