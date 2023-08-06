from typing import Union
from datetime import datetime as dt
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.sqlite import JSON


Base = declarative_base()


class Sensor(Base):
    __tablename__ = 'sensors'

    # columns
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64), nullable=False)
    payload = sa.Column(MutableDict.as_mutable(JSON), nullable=False, default={})
    pub_key = sa.Column(sa.String, nullable=True)

    created = sa.Column(sa.DateTime, default=dt.utcnow)
    updated = sa.Column(sa.DateTime, default=dt.utcnow, onupdate=dt.utcnow)
    last_seen = sa.Column(sa.DateTime)

    # relations
    raw_data = sa.orm.relationship('Raw', back_populates='sensor', cascade='all, delete')

    def __init__(self, id=None, name=None, payload=None, pub_key=None, created=None, updated=None, last_seen=None, **kwargs):
        # update the config with all data
        payload.update(kwargs)
        super(Sensor, self).__init__(id=id, name=name, payload=payload, pub_key=pub_key, created=created, updated=updated, last_seen=last_seen)

    @classmethod
    def exists(cls, session: sa.orm.Session, other: Union[int, str, 'Sensor']):
        # build base query
        query = session.query(cls)

        # filter
        if isinstance(other, int):
            query = query.filter(cls.id==other)
        elif isinstance(other, str):
            query = query.filter(cls.name.like(other))
        elif isinstance(other, cls):
            query = query.filter(cls.id==other.id)

        return query.first() is not None
    
    def __str__(self):
        pay = ' '.join([f'{k}={v}' for k, v in self.payload.items()])

        # has config
        if len(pay) > 0:
            pay = ' ' + pay
        
        # did measure
        if self.last_seen is not None:
            elapsed = (dt.utcnow() - self.last_seen).seconds
            unit = 'sec'
            if elapsed > 180:
                elapsed /= 60
                unit = 'min'
                if elapsed > 120:
                    elapsed /= 60
                    unit = 'hours'
                    if elapsed > 72:
                        elapsed /= 24
                        unit = 'days'
            elapsed = f' - last seen {round(elapsed)} {unit} ago'
        else:
            elapsed = ''

        return f"<ID={self.id}> {self.name}{pay}{elapsed}"
    
    def json(self) -> dict:
        d = {
            'id': self.id,
            'name': self.name,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            'last_seen': self.last_seen.isoformat() if self.last_seen is not None else 'never',
            **self.payload
        }

        if self.pub_key is not None:
            d['pub_key'] = self.pub_key

        return d


class Raw(Base):
    __tablename__ = 'raw'

    # columns
    sensor_id = sa.Column(sa.Integer, sa.ForeignKey('sensors.id'), primary_key=True)
    tstamp = sa.Column(sa.DateTime, primary_key=True)
    payload = sa.Column(MutableDict.as_mutable(JSON), nullable=False)

    # realtions
    sensor = sa.orm.relationship('Sensor', back_populates='raw_data')

    def __str__(self):
        if len(self.payload.keys()) > 0:
            pay = ' '.join([f'{k}={v}' for k, v in self.payload.items()])
        else:
            pay = 'empty message'
        return f"[{self.tstamp.isoformat()}] {pay}"
    
    def json(self, include_sensor=False):
        d =   {
            'tstamp': self.tstamp.isoformat(),
            **self.payload
        }

        if include_sensor:
            d.update(**{f'sensor_{k}':v for k, v in self.sensor.json().items()})
        
        return d
