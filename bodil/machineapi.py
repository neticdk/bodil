from flask.ext.restful import Resource
from flask.ext.restful import fields, marshal_with
from flask.ext.restful import reqparse, abort

from .util import abort_if_invalid_mac_address
from .machine import get_machine
from .machine import Machine, Machines, MissingMachineField

required_fields = ['mac', 'name', 'profile', 'ip', 'gw', 'dns']
optional_fields = ['coreos_etcd_token', 'repo_url', 'ntp']
other_fields = ['coreos_channel', 'coreos_version', 'coreos_etcd_enabled',
                'coreos_etcd_role', 'state', '_hack', 'meta', 'sshkeys']
all_fields = required_fields+optional_fields+other_fields

meta_fields = {
    'git_ref': fields.String,
    'deployed_by': fields.String,
    'deployed_time': fields.Integer
}

machines_fields = {
    'mac': fields.String,
    'href': fields.Url('machine')
}

machine_fields = {
    'name': fields.String,
    'mac': fields.String,
    'profile': fields.String,
    'ip': fields.String,
    'gw': fields.String,
    'dns': fields.String,
    'ntp': fields.String,
    'coreos_channel': fields.String,
    'coreos_version': fields.String,
    'coreos_etcd_token': fields.String,
    'coreos_etcd_enabled': fields.Boolean,
    'coreos_etcd_role': fields.String,
    'sshkeys': fields.List(fields.String),
    'state': fields.String,
    'repo_url': fields.String,
    '_hack': fields.String,
    'meta': fields.Nested(meta_fields)
}


class MachinesAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        for f in required_fields:
            self.reqparse.add_argument(f, type=str, required=True)
        for f in optional_fields:
            self.reqparse.add_argument(f, type=str, required=False)
        self.reqparse.add_argument('sshkeys', type=list, default=[], location='json')
        self.reqparse.add_argument('coreos_etcd_enabled', type=bool, default=False)
        self.reqparse.add_argument('coreos_etcd_role', type=str, default='member')
        self.reqparse.add_argument('coreos_channel', type=str, default='stable')
        self.reqparse.add_argument('coreos_version', type=str, default='current')
        self.reqparse.add_argument('state', type=str,
                                   default='READY-FOR-DEPLOYMENT')
        self.reqparse.add_argument('_hack', type=str, default='')
        self.reqparse.add_argument('meta', type=dict, default={})
        super(MachinesAPI, self).__init__()

    @marshal_with(machines_fields)
    def get(self):
        return Machines.list()

    @marshal_with(machine_fields)
    def post(self):
        args = self.reqparse.parse_args(strict=True)
        abort_if_invalid_mac_address(args['mac'])
        machine = Machine(**args)
        if machine.exists():
            abort(409)

        try:
            machine.save()
        except MissingMachineField as e:
            abort(400, message=str(e))

        return machine, 201

class MachineAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        for f in required_fields:
            self.reqparse.add_argument(f, type=str, store_missing=False)
        for f in optional_fields:
            self.reqparse.add_argument(f, type=str, store_missing=False)
        self.reqparse.add_argument('sshkeys', type=list, default=[], location='json', store_missing=False)
        self.reqparse.add_argument('coreos_etcd_enabled', type=bool, default=False, store_missing=False)
        self.reqparse.add_argument('coreos_etcd_role', type=str, default='member', store_missing=False)
        self.reqparse.add_argument('coreos_channel', type=str, store_missing=False)
        self.reqparse.add_argument('coreos_version', type=str, store_missing=False)
        self.reqparse.add_argument('state', type=str, store_missing=False)
        self.reqparse.add_argument('meta', type=dict, store_missing=False)
        #for f in all_fields:
        #    self.reqparse.add_argument(f, type=str, store_missing=False)
        super(MachineAPI, self).__init__()

    @marshal_with(machine_fields)
    def get(self, mac):
        abort_if_invalid_mac_address(mac)
        machine = get_machine(mac)
        return machine

    @marshal_with(machine_fields)
    def put(self, mac):
        abort_if_invalid_mac_address(mac)
        args = self.reqparse.parse_args(strict=True)
        machine = get_machine(mac)
        for k, v in args.items():
            if k == '_hack':
                continue
            if v != getattr(machine, k):
                setattr(machine, k, v)
            elif isinstance(v, dict):
                setattr(machine, k, v)
        try:
            machine.save()
        except MissingMachineField as e:
            abort(400, message=str(e))

        return machine

    def delete(self, mac):
        abort_if_invalid_mac_address(mac)
        machine = get_machine(mac)
        machine.destroy()
        return '', 204
