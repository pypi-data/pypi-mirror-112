import fire 

from .web import start
from .api.cli import SensorCli, PayloadCli, DebugCli


# spin up API
fire.Fire({
    'web': start,
    'sensor': SensorCli,
    'payload': PayloadCli,
    'virtual-payload': DebugCli
})
