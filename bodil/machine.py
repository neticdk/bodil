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
        self.coreos_channel = kwargs.pop('coreos_channel', None)
        self.coreos_version = kwargs.pop('coreos_version', None)
        self.state = kwargs.pop('state', None)
        self.repo_url = kwargs.pop('repo_url', None)
        self.meta = kwargs.pop('meta', {})

    def load(self):
        try:
            with open("machines/{}.json".format(self.mac), 'r') as infile:
                data = json.load(infile)
                self.name = data.get('name')
                self.profile = data.get('profile')
                self.ip = data.get('ip', None)
                self.gw = data.get('gw', None)
                self.dns = data.get('dns', None)
                self.sshkey = data.get('sshkey', None)
                self.etcd_token = data.get('etcd_token', None)
                self.coreos_channel = data.get('coreos_channel', None)
                self.coreos_version = data.get('coreos_version', None)
                self.state = data.get('state', None)
                self.repo_url = data.get('repo_url', None)
                self.meta = data.get('meta', {})
        except IOError as e:
            if e.errno == errno.ENOENT:
                raise MachineNotFound
            raise

    def validate(self):
        for f in ['name', 'profile']:
            # , 'ip', 'gw', 'dns', 'state']:
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
                    'coreos_channel': self.coreos_channel,
                    'coreos_version': self.coreos_version,
                    'state': self.state,
                    'repo_url': self.repo_url,
                    'meta': self.meta
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
