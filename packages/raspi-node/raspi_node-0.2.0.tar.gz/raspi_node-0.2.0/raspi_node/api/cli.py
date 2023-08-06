from typing import Union

from . import collection
from ..db import get_session
from ..util import dict_to_csv, debug_sensor


class SensorCli:
    def __init__(self, json=False):
        # store a session
        self.session = get_session()
        self.json = json

    def get(self, id_or_name: Union[int, str]):
        sensor = collection.get_sensor(id_or_name)
        if sensor is None:
            return f'Sensor {id_or_name} not found.'
        
        if self.json:
            return sensor.json()
        else:
            return str(sensor)
    
    def create(self, name: str, pub_key: str = None, **kwargs):
        sensor = collection.create_sensor(name=name, pub_key=pub_key, session=self.session, **kwargs)

        if self.json:
            return sensor.json()
        else:
            return str(sensor)

    def update(self, name: str, **kwargs):
        sensor = collection.update_sensor(id_or_name=name, session=self.session, **kwargs)

        if self.json:
            return sensor.json()
        else:
            return str(sensor)

    def delete(self, name: str):
        collection.delete_sensor(id_or_name=name, session=self.session)
        return f"Deleted Sensor {name}"


class PayloadCli:
    def __init__(self, json=False, csv=False):
        # store a session
        self.session = get_session()
        self.json = json
        self.csv = csv
    
    def save(self, sensor: str, *message, **payload):
        if len(message) > 0:
            payload = message[0]
        sensor = collection.save_payload(sensor_id_or_name=sensor, payload=payload, session=self.session)

        if self.json:
            return sensor.json()
        else:
            return str(sensor)
    
    def read(self, sensor: str = None, since: str = None, before: str = None, limit: int = None, omit_sensor=False, delimiter=',', header=True):
        readings = collection.read_payload(sensor_id_or_name=sensor, since=since, before=before, limit=limit)

        if self.json:
            return [r.json(include_sensor= not omit_sensor) for r in readings]
        elif self.csv:
            return dict_to_csv([r.json(include_sensor= not omit_sensor) for r in readings], delimiter=delimiter, header=header)
        else:
            return readings
    
    def delete(self, sensor: str = None, since: str = None, before: str = None, limit: int = None):
        n = collection.delete_payload(sensor_id_or_name=sensor, session=self.session, since=since, before=before, limit=limit)
        return f"Deleted {n} payloads."


class DebugCli:
    def __call__(self, sensor: str = None, step: int = 60, random_type: str = 'walk', endpoint: str = 'cli', limit: int = 150, **kwargs):
        debug_sensor(sensor_id=sensor, step=step, random_type=random_type, endpoint=endpoint, limit=limit, verbose=True, **kwargs)
