import json
import errno
import os.path

from flask.ext.restful import abort

from .util import is_valid_mac_address


class MachineNotFound(Exception):
    pass


class MissingMachineField(Exception):
    pass


class Machine(object):
    def __init__(self, **kwargs):
        self.mac = kwargs.pop('mac')
        self.name = kwargs.pop('name', None)
        self.profile = kwargs.pop('profile', None)
        self.ip = kwargs.pop('ip', None)
        self.gw = kwargs.pop('gw', None)
        self.dns = kwargs.pop('dns', None)
        self.sshkey = kwargs.pop('sshkey', None)
        self.etcd_token = kwargs.pop('etcd_token', None)
        self.state = kwargs.pop('state', None)

    def load(self):
        try:
            with open("machines/{}.json".format(self.mac), 'r') as infile:
                data = json.load(infile)
                self.name = data.get('name')
                self.profile = data.get('profile')
                self.ip = data.get('ip')
                self.gw = data.get('gw')
                self.dns = data.get('dns')
                self.sshkey = data.get('sshkey', None)
                self.etcd_token = data.get('etcd_token', None)
                self.state = data.get('state', None)
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise MachineNotFound
            raise

    def validate(self):
        for f in ['name', 'profile', 'ip', 'gw', 'dns', 'state']:
            if getattr(self, f) is None:
                raise MissingMachineField("{} must not be null".format(f))

    def save(self):
        self.validate()
        try:
            with open("machines/{}.json".format(self.mac), 'w') as outfile:
                data = {
                    'name': self.name,
                    'profile': self.profile,
                    'ip': self.ip,
                    'gw': self.gw,
                    'dns': self.dns,
                    'sshkey': self.sshkey,
                    'etcd_token': self.etcd_token,
                    'state': self.state
                }
                json.dump(data, outfile)
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise MachineNotFound
            raise

    def destroy(self):
        os.remove("machines/{}.json".format(self.mac))

    def exists(self):
        return os.path.isfile("machines/{}.json".format(self.mac))


def get_machine(mac):
    m = Machine(mac=mac)
    try:
        m.load()
    except MachineNotFound:
        abort(404)
    return m


class Machines(object):
    @staticmethod
    def list():
        result = []
        for f in os.listdir("machines"):
            fname = os.path.splitext(f)[0]
            if is_valid_mac_address(fname):
                result.append({'mac': fname})
        return result