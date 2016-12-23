from flask import render_template
from flask.ext.restful import Resource

import bodil
from .machine import get_machine
from .util import (abort_if_invalid_mac_address, plaintext_response,
                  bits_to_quads)


class KickstartAPI(Resource):
    def get(self, mac):
        abort_if_invalid_mac_address(mac)
        machine = get_machine(mac)

        dns = getattr(machine, 'dns', '')
        if dns is None:
            dns = ''
        dns = dns.split(',')
        ip_domain = machine.name.partition('.')[2]

        ntp = getattr(machine, 'ntp', '')
        if ntp is None:
            ntp = ''
        ntp = ntp.split(',')

        nics = [cidr2ipinfo(nic) for nic in getattr(machine, 'nics', [])]

        try:
            nics[machine.default_gw_idx]['gw'] = machine.default_gw
        except IndexError:
            pass

        template_fields = dict(
            base_url=bodil.BODIL_URL,
            name=machine.name,
            mac=mac,
	    nics=nics,
	    dns=dns,
            ntp=ntp,
            default_gw=machine.default_gw,
	    default_gw_idx=machine.default_gw_idx,
            ip_domain=ip_domain,
	    sshkeys=machine.sshkeys,
            meta=machine.meta,
            repo_url=machine.repo_url
        )

        template = 'kickstart-{}'.format(machine.profile)
        res = plaintext_response(render_template(template, **template_fields))
        return res
