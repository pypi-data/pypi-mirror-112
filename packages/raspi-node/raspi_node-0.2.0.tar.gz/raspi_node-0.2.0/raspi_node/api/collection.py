from typing import Union, List
from datetime import datetime as dt

from sqlalchemy.orm import Session
from dateutil.parser import parse

from ..db import get_session
from .. import models


def get_sensor(id_or_name: Union[int, str], session: Session = None) -> models.Sensor:
    """
    Get a sensor from the database
    """
    # get a session
    if session is None:
        session = get_session()

    # build query
    if isinstance(id_or_name, int):
        return session.query(models.Sensor).filter(models.Sensor.id==id_or_name).first()
    else:
        id_or_name = id_or_name.replace('*', '%')
        return session.query(models.Sensor).filter(models.Sensor.name.like(id_or_name)).first()


def create_sensor(name: str, session: Session = None, payload: dict = {}, pub_key: str = None, **kwargs) -> models.Sensor:
    # create
    sensor = models.Sensor(name=name, payload=payload, pub_key=pub_key, **kwargs)

    # open an session
    if session is None:
        session = get_session()

    try:
        session.add(sensor)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return sensor


def update_sensor(id_or_name: Union[int, str], session: Session = None, **kwargs) -> models.Sensor:
    # create a session
    if session is None:
        session = get_session()

    # get the sensor
    sensor = get_sensor(id_or_name=id_or_name, session=session)

    if sensor is None:
        return None

    # update
    for key, value in kwargs.items():
        if hasattr(sensor, key):
            setattr(sensor, key, value)
        else:
            # add to payload
            sensor.payload.update({key: value})
    
    # save
    try:
        session.add(sensor)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
    return sensor


def delete_sensor(id_or_name: Union[int, str], session: Session = None) -> None:
    # get a session
    if session is None:
        session = get_session()

    # load sensor
    sensor = get_sensor(id_or_name=id_or_name, session=session)

    try:
        session.delete(sensor)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e


def save_payload(sensor_id_or_name: Union[int, str], payload: Union[str, dict], session: Session = None) -> models.Sensor:
    # get a session
    if session is None:
        session = get_session()

    # get the sensor
    sensor = get_sensor(id_or_name=sensor_id_or_name, session=session)

    if sensor is None:
        # TODO: replace by Custom exception
        raise RuntimeError(f'A Sensor {sensor_id_or_name} is not known')
    
    # create payload
    if isinstance(payload, str):
        payload = dict(sensor=sensor.name, message=payload)
    
    # create a consistent timestamp
    tstamp = dt.utcnow()

    # create the raw message log
    log = models.Raw(sensor_id=sensor.id, tstamp=tstamp, payload=payload)

    # update the sensor, that it was seen
    sensor.last_seen = tstamp

    # save
    try:
        session.add(log)
        session.add(sensor)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    
    return sensor


def read_payload(
    sensor_id_or_name: Union[int, str, list] = None,
    session: Session = None,
    since: Union[str, dt] = None,
    before: Union[str, dt] = None,
    limit: int = None,
    return_iterator = False
) -> List[models.Raw]:
    # get a session
    if session is None:
        session = get_session()

    # build the base query
    query = session.query(models.Raw)

    # check which sensors are needed
    if sensor_id_or_name is not None:
        # make it a list
        if not isinstance(sensor_id_or_name, (list, tuple)):
            sensor_id_or_name = [sensor_id_or_name]
        
        # get ids
        sensor_ids = [get_sensor(id_or_name, session=session).id for id_or_name in sensor_id_or_name]

        # filter
        if len(sensor_ids) > 0:
            query = query.filter(models.Raw.sensor_id.in_(sensor_ids))
    
    # add date filters
    if since is not None:
        # convert strings
        if isinstance(since, str):
            since = parse(since)
        query = query.filter(models.Raw.tstamp >= since)

    if before is not None:
        # convert strings
        if isinstance(before, str):
            before = parse(before)
        query = query.filter(models.Raw.tstamp <= before)
    
    # order
    query = query.order_by(models.Raw.tstamp.desc())

    # limit
    if limit is not None:
        query = query.limit(limit)
    
    # check return
    if return_iterator:
        return query
    else:
        return query.all()


def delete_payload(
    sensor_id_or_name: Union[int, str, list] = None,
    session: Session = None,
    since: Union[str, dt] = None,
    before: Union[str, dt] = None,
    limit: int = None,
    return_iterator = False
) -> int:
    # get a session
    if session is None:
        session = get_session()
    
    # read the payloads
    payloads = read_payload(sensor_id_or_name=sensor_id_or_name, session=session,since=since, before=before, limit=limit)
    n = len(payloads)

    try:
        for payload in payloads:
            session.delete(payload)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

    return n   

