import sys
import json
from tornado import web
from tornado import ioloop

from . import api
from .db import get_session
from . import __version__, LIBPATH


# build base JSON response class
class JsonRequestHandler(web.RequestHandler):
    def set_default_headers(self) -> None:
        self.set_header('Content-Type', 'application/json')


# main class
class MainHandler(JsonRequestHandler):
    def get(self):
        self.write({
            'message': 'Raw data is awesome!',
            'version': __version__,
            'libpath': LIBPATH,
            'python': sys.executable,
            'python_version': sys.version
        })


# sensor class
class SensorHandler(JsonRequestHandler):
    def initialize(self):
        self.session = get_session()

    def parse_id(self, id_or_name):
        try:
            id_or_name = int(id_or_name)
        except Exception:
            pass
        return id_or_name

    def get(self, id_or_name):
        name = self.parse_id(id_or_name)
        sensor = api.collection.get_sensor(id_or_name=name)
        self.write(sensor.json())
        
    def put(self, name):
        name = self.parse_id(name)

        # get the body
        body = json.loads(self.request.body)
        if isinstance(name, int):
            name = body.get('name', 'Unknown Sensor')

        # extract public key
        pub_key = body.get('pub_key')

        payload = {k: v for k, v in body.items() if k not in ('name', 'pub_key')}

        # create the instance
        sensor = api.collection.create_sensor(name, session=self.session, payload=payload, pub_key=pub_key)

        self.write(sensor.json())

    def post(self, id_or_name):
        # parse
        name = self.parse_id(id_or_name)

        # get the body
        body = json.loads(self.request.body)

        # update the sensor
        sensor = api.collection.update_sensor(name, session=self.session, **body)

        self.write(sensor.json())

    def delete(self, id_or_name):
        # parse
        name = self.parse_id(id_or_name)

        # delete
        api.collection.delete_sensor(name, session=self.session)

        self.write({'message': f'Sensor {name} deleted.'})


# payload class
class PayloadHandler(JsonRequestHandler):
    def initialize(self):
        self.session = get_session()

    def parse_id(self, id_or_name):
        try:
            id_or_name = int(id_or_name)
        except Exception:
            pass
        return id_or_name

    def get(self, id_or_name):
        # sensor name
        sensor_id = self.parse_id(id_or_name)
        sensor = api.collection.get_sensor(sensor_id)

        if sensor is None:
            self.write({'message': f'Sensor {sensor_id} not found.'})
        
        # get the arguments
        since = self.get_argument('since', None)
        before = self.get_argument('before', None)
        limit = self.get_argument('limit', None)

        # read the database
        readings = api.collection.read_payload(sensor_id, self.session, since=since, before=before, limit=limit)

        self.write({
            'sensor': sensor.json(),
            'payloads': [r.json() for r in readings]
        })
    
    def put(self, id_or_name):
        # sensor name
        sensor_id = self.parse_id(id_or_name)

        # get the payload
        try:
            payload = json.loads(self.request.body)
        except json.JSONDecodeError:
            payload = self.request.body.decode()
        
        # save
        sensor = api.collection.save_payload(sensor_id, payload=payload, session=self.session)

        # get last
        payload = api.collection.read_payload(sensor.id, self.session, limit=1)[0]

        self.write({
            'sensor': sensor.json(),
            'payload': payload.json()
        })

    def delete(self, id_or_name):
        # sensor name
        sensor_id = self.parse_id(id_or_name)

        # get the arguments
        since = self.get_argument('since', None)
        before = self.get_argument('before', None)
        limit = self.get_argument('limit', None)

        deleted = api.collection.delete_payload(sensor_id, self.session, since=since, before=before, limit=limit) 

        self.write({'message': f'Deleted {deleted} payload messages.'})


def make_app(debug=False) -> web.Application:
    app = web.Application(
        handlers=[
            ('/', MainHandler),
            (r'/sensor/([^/]+)', SensorHandler),
            (r'/payload/([^/]+)', PayloadHandler),
        ],
        debug=debug
    )

    return app


def start(port=8888, debug=False):
    """
    Start the webserver on given port
    """
    # get the application
    app = make_app(debug=debug)

    # listen to specified port
    app.listen(port=port)

    # go into io loop
    ioloop.IOLoop().current().start()
