from flask import render_template
from flask.ext.restful import Resource

import bodil
from .machine import get_machine
from .util import (abort_if_invalid_mac_address, plaintext_response,
                  bits_to_quads)


class PreseedAPI(Resource):
    def get(self, mac):
        abort_if_invalid_mac_address(mac)
        machine = get_machine(mac)

        template = 'preseed-{}'.format(machine.profile)

        ip_addr = None
        ip_prefix = None
        ip_netmask = None
        ip_gw = getattr(machine, 'gw', None)
        if ip_gw == '':
          ip_gw = None

        ip_cidr = getattr(machine, 'ip', None)
        if ip_cidr != '' and ip_cidr is not None and '/' in ip_cidr:
            ip_addr, ip_prefix = (ip_cidr.split('/') + [None])[:2]
            ip_netmask = bits_to_quads(int(ip_prefix))

        dns = getattr(machine, 'dns', '')
        if dns is None:
            dns = ''
        ip_dns = dns.split(',')
        ip_domain = machine.name.partition('.')[2]

        res = plaintext_response(render_template(
            template,
            name=machine.name,
            base_url=bodil.BODIL_URL,
	    ip_addr=ip_addr,
            ip_prefix=ip_prefix,
            ip_netmask=ip_netmask,
            ip_gw=ip_gw,
	    ip_dns=ip_dns,
            ip_domain=ip_domain,
            repo_url=machine.repo_url,
            meta=machine.meta,
            mac=mac))
        return res
