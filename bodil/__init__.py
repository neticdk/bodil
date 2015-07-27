import os
import socket

from flask import Flask
from flask.ext.restful import Api

from .bootapi import BootAPI
from .cloudconfigscriptapi import CloudConfigScriptAPI
from .cloudconfigapi import CloudConfigAPI
from .machineapi import MachineAPI, MachinesAPI

app = Flask(__name__)
api = Api(app)

BODIL_PORT = int(os.environ.get('BODIL_PORT', 5000))
BODIL_DEFAULT_URL = 'http://{}:{}'.format(
    socket.gethostbyname(socket.gethostname()), BODIL_PORT)
BODIL_DEBUG = bool(os.environ.get('BODIL_DEBUG', False))
BODIL_URL = os.environ.get('BODIL_BASE_URL', BODIL_DEFAULT_URL)


# TODO: support create, delete, update
api.add_resource(BootAPI, '/api/v1/boot/<string:mac>')
# TODO: support create, delete, update
api.add_resource(CloudConfigScriptAPI,
                 '/api/v1/cloud-config-script/<string:mac>')
# TODO: support create, delete, update
api.add_resource(CloudConfigAPI, '/api/v1/cloud-config/<string:mac>')
api.add_resource(MachineAPI, '/api/v1/machine/<string:mac>', endpoint='machine')
api.add_resource(MachinesAPI, '/api/v1/machine')
