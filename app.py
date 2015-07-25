import json
import re
import os
import os.path
import socket

from flask import Flask
from flask import request
from flask import abort
from flask import render_template
from flask import jsonify

app = Flask(__name__)

my_ip = socket.gethostbyname(socket.gethostname())
bodil_port = int(os.environ.get('BODIL_PORT', 5000))
base_url = os.environ.get('BODIL_BASE_URL', 'http://{}:{}'.format(my_ip,
                                                                  bodil_port))


def valid_mac(mac):
    return re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",
                    mac.lower())


@app.route('/boot/<mac>', methods=['GET'])
def get_bootscript(mac):
    if not valid_mac(mac):
        abort(400)

    if not os.path.isfile("machines/{}.json".format(mac)):
        abort(404)

    with open("machines/{}.json".format(mac), 'r') as infile:
        data = json.load(infile)

    return render_template('boot-{}.ipxe'.format(data['profile']),
                           base_url=base_url)


@app.route('/cloud-config-script/<mac>', methods=['GET'])
def get_cloud_config_script(mac):
    if not valid_mac(mac):
        abort(400)

    if not os.path.isfile("machines/{}.json".format(mac)):
        abort(404)

    return render_template('install-coreos.sh', base_url=base_url, mac=mac)


@app.route('/cloud-config/<mac>', methods=['GET'])
def get_cloud_config(mac):
    if not valid_mac(mac):
        abort(400)

    if not os.path.isfile("machines/{}.json".format(mac)):
        abort(404)

    with open("machines/{}.json".format(mac), 'r') as infile:
        data = json.load(infile)

    return render_template('cloud-config-{}.yml'.format(data['profile']),
                           ip=data['ip'], gw=data['gw'], dns=data['dns'],
                           name=data['name'], sshkey=data['sshkey'],
                           etcd_token=data['etcd_token'])


@app.route('/machine/<mac>', methods=['GET'])
def get_machine(mac):
    if not valid_mac(mac):
        abort(400)

    if not os.path.isfile("machines/{}.json".format(mac)):
        abort(404)

    with open("machines/{}.json".format(mac), 'r') as infile:
        data = json.load(infile)

    # FIXME: stupid, I was lazy
    return jsonify(data)


@app.route('/machine/<mac>', methods=['PUT'])
def set_machine(mac):
    if not valid_mac(mac):
        abort(400)

    if not os.path.isfile("machines/{}.json".format(mac)):
        abort(404)

    with open("machines/{}.json".format(mac), 'r') as infile:
        data = json.load(infile)

    state = request.form.get('state', None)

    if state is None:
        abort(400)

    data['state'] = state

    with open("machines/{}.json".format(mac), 'w') as outfile:
        json.dump(data, outfile)

    return jsonify(data)


@app.route('/machine', methods=['POST'])
def create_machine():
    mac = request.form.get('mac', None)
    name = request.form.get('name', None)
    ip = request.form.get('ip', None)
    gw = request.form.get('gw', None)
    dns = request.form.get('dns', None)
    profile = request.form.get('profile', 'default')
    sshkey = request.form.get('sshkey', None)
    etcd_token = request.form.get('etcd_token', None)
    state = 'READY_FOR_DEPLOYMENT'
    if mac is None or name is None or ip is None or gw is None or dns is None:
        abort(400)

    if not valid_mac(mac):
        abort(400)

    if os.path.isfile("machines/{}.json".format(mac)):
        abort(409)

    machine = dict(mac=mac, ip=ip, gw=gw, dns=dns, name=name, profile=profile,
                   sshkey=sshkey, state=state, etcd_token=etcd_token)
    with open("machines/{}.json".format(mac), 'w') as outfile:
        json.dump(machine, outfile)

    return jsonify(machine)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=bodil_port, debug=True)
