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

        template = 'kickstart-{}'.format(machine.profile)
        ip, ip_mask = getattr(machine, 'ip', '/32').split('/')
        netmask = bits_to_quads(int(ip_mask))
        nameservers = getattr(machine, 'dns', '').split(',')
        domainname = machine.name.partition('.')[2]
        res = plaintext_response(render_template(
            template, base_url=bodil.BODIL_URL, name=machine.name,
	    ip_addr=ip, ip_mask=ip_mask, ip_netmask=netmask, ip_gw=machine.gw,
	    ip_dns=nameservers, ip_domain=domainname,
            repo_url=machine.repo_url, mac=mac))
        return res
