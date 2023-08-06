from time import sleep

import pytest

import kamzik3
from kamzik3.devices.deviceSession import DeviceSession


session_config = {'attributes': {('Log directory', 'Value'): './kamzik3/test/server_log',
                                 ('Resource directory', 'Value'): './kamzik3/test/resources',
                                 ('Allow attribute log', 'Value'): False}}
DeviceSession(device_id="Device_Session", config=session_config)
sleep(3)
print("now")
kamzik3.session.stop()
