from flask import render_template
from flask.ext.restful import Resource

import bodil
from .machine import get_machine
from .util import (abort_if_invalid_mac_address, plaintext_response,
                  bits_to_quads)


class CloudConfigAPI(Resource):
    def get(self, mac):
        abort_if_invalid_mac_address(mac)
        machine = get_machine(mac)

        dns = getattr(machine, 'dns', '')
        if dns is None:
            dns = ''
        dns = dns.split(',')

        ntp = getattr(machine, 'ntp', '')
        if ntp is None:
            ntp = ''
        ntp = ntp.split(',')

        ip_addr = None
        ip_prefix = None
        ip_netmask = None
        ip_cidr = getattr(machine, 'ip', None)
        if ip_cidr:
            ip_addr, ip_prefix = (ip_cidr.split('/') + [None])[:2]
            ip_netmask = bits_to_quads(int(ip_prefix))

        template_fields = dict(base_url=bodil.BODIL_URL, ip=machine.ip,
			       ip_addr=ip_addr, ip_prefix=ip_prefix,
                               ip_netmask=ip_netmask,
                               gw=machine.gw, dns=dns, ntp=ntp,
                               name=machine.name, sshkeys=machine.sshkeys,
                               coreos_etcd_token=machine.coreos_etcd_token,
                               coreos_etcd_enabled=machine.coreos_etcd_enabled,
                               coreos_etcd_role=machine.coreos_etcd_role)

        template = 'cloud-config-{}.yml'.format(machine.profile)
        res = plaintext_response(render_template(template, **template_fields))
        return res
