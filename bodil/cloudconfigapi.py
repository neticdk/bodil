from flask import render_template
from flask.ext.restful import Resource

import bodil
from .machine import get_machine
from .util import (abort_if_invalid_mac_address, plaintext_response,
                  cidr2ipinfo)


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

        nics = [cidr2ipinfo(nic) for nic in getattr(machine, 'nics', [])]

        try:
            nics[machine.default_gw_idx]['gw'] = machine.default_gw
        except IndexError:
            pass

        template_fields = dict(base_url=bodil.BODIL_URL, nics=nics,
			       default_gw=machine.default_gw,
			       default_gw_idx=machine.default_gw_idx,
                               dns=dns, ntp=ntp, name=machine.name,
			       sshkeys=machine.sshkeys,
                               coreos_etcd_token=machine.coreos_etcd_token,
                               coreos_etcd_enabled=machine.coreos_etcd_enabled,
                               coreos_etcd_role=machine.coreos_etcd_role)

        template = 'cloud-config-{}.yml'.format(machine.profile)
        res = plaintext_response(render_template(template, **template_fields))
        return res
