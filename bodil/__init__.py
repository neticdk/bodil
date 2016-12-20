import os
import socket

from flask import Flask
from flask.ext.restful import Api

from .bootapi import BootAPI
from .cloudconfigscriptapi import CloudConfigScriptAPI
from .cloudconfigapi import CloudConfigAPI
from .machineapi import MachineAPI, MachinesAPI
from .kickstartapi import KickstartAPI
from .preseedapi import PreseedAPI


BODIL_PORT = int(os.environ.get('BODIL_PORT', 5000))
BODIL_DEFAULT_URL = 'http://{}:{}'.format(
    socket.gethostbyname(socket.gethostname()), BODIL_PORT)
BODIL_DEBUG = bool(os.environ.get('BODIL_DEBUG', False))
BODIL_URL = os.environ.get('BODIL_BASE_URL', BODIL_DEFAULT_URL)
BODIL_TEMPLATE_FOLDER = os.environ.get('BODIL_TEMPLATE_FOLDER', 'templates')

app = Flask(__name__, template_folder=BODIL_TEMPLATE_FOLDER)
api = Api(app)

app.debug = BODIL_DEBUG

# TODO: support create, delete, update
api.add_resource(BootAPI, '/api/v1/boot/<string:mac>')
# TODO: support create, delete, update
api.add_resource(CloudConfigScriptAPI,
                 '/api/v1/cloud-config-script/<string:mac>')
# TODO: support create, delete, update
api.add_resource(CloudConfigAPI, '/api/v1/cloud-config/<string:mac>')
api.add_resource(MachineAPI, '/api/v1/machine/<string:mac>', endpoint='machine')
api.add_resource(MachinesAPI, '/api/v1/machine')

api.add_resource(KickstartAPI, '/api/v1/kickstart/<string:mac>')
api.add_resource(PreseedAPI, '/api/v1/preseed/<string:mac>')
