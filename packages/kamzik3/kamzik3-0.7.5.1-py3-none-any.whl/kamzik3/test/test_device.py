import pytest

import kamzik3
from kamzik3.constants import *
from kamzik3.devices.device import Device


@pytest.fixture
def device():
    yield Device(device_id="test_device", config=None)


def test_device_creation(device):
    assert device.device_id == "test_device"
    assert device.session is kamzik3.session
    assert device.get_value(ATTR_ID) == "test_device"


@pytest.mark.parametrize("status", STATUSES_PRIORITY)
def test_device_status(device, status):
    device.set_status(status)
    assert device.get_value(ATTR_STATUS) == status
