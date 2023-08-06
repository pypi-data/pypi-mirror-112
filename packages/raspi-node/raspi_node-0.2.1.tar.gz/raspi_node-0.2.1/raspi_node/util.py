from typing import Union, List
from random import random
from time import sleep
import json
import os
import requests
from datetime import datetime as dt


def dict_to_csv(d: Union[dict, List[dict]], delimiter=',', quote=False, na_value='nan', header=True, deep=True) -> str:
    # turn dict to list
    if isinstance(d, dict):
        d = [d]

    # get all keys
    if deep:
        headers = []
        for el in d:
            for k in list(el.keys()):
                if k not in headers:
                    headers.append(k)
    else:
        headers = list(d[0].keys())

    # build the csv
    csv = [f'{delimiter}'.join([str(el.get(k, na_value)) for k in headers]) for el in d]

    if header:
        return "%s\n%s" % (f'{delimiter}'.join(headers), '\n'.join(csv))
    else:
        return '\n'.join(csv)


def debug_sensor(
    sensor_id: int,
    step: int = 60,
    payload_template: dict = {
        'debug': True,
        'message': 'Random artificial data'
    },
    random_type: str = 'walk',
    endpoint: str = 'cli',
    limit: int = 150,
    verbose = False,
    **kwargs
):
    """
    Starts an artificial sensor node that sends random data to the API or web.

    """
    # check the type of random required.
    if random_type == 'walk':
        values = [random() *2 - 1]
        
        # define the value generator
        def gen() -> float:
            v = (random() * 2 - 1) + values[-1]
            values.append(v)
            return v
    
    # TOD: place more options here
    else:
        gen = lambda: random() * 2 - 1
    
    # start the main loop
    i = 0
    
    while limit is None or i < limit:
        # increment
        i += 1

        # add a new value
        payload = {**payload_template, 'value': round(gen(), 3), 'iteration': i, 'time': dt.now().isoformat()}
        if verbose:
            print("Send payload: %s" % (json.dumps(payload)))
        
        # check endpoint
        if endpoint == 'cli':
            # run
            payload_args = ' '.join([f'--{k} {v}' if isinstance(v, (int, float)) else f'--{k} "{v}"' for k, v in payload.items()])
            cmd = f"python -m raspi_node payload save {sensor_id} {payload_args}"
            os.system(cmd)
            if verbose:
                print(cmd)
        
        # use WEB
        elif endpoint == 'web':
            # get the host
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 8888)
            url = f"http://{host}:{port}/payload/{sensor_id}"
            
            if verbose:
                print(f"connecting {url}...", end='')
            
            # request
            response = requests.put(url, json=payload)
            
            if verbose:
                if response.status_code < 400:
                    print('done.')
                else:
                    print(f'ERROR.\n{response.content}')

        # finally sleep
        if verbose:
            print("Go to sleep, see you in %d seconds." % step)
        
        sleep(step)
