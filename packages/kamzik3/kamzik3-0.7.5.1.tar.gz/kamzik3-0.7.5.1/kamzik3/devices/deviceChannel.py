from kamzik3.constants import *
from kamzik3.devices.device import Device
from kamzik3.devices.observer import Observer


class DeviceChannel(Device, Observer):

    def __init__(self, device, channel, device_id=None, config=None):
        self.configured = False
        self.device = device
        self.channel = channel
        self.position_attribute_copy = None
        super(DeviceChannel, self).__init__(device_id, config)
        self.set_status(STATUS_CONNECTING)
        self.device.attach_observer(self)

    def _init_attributes(self):
        Device._init_attributes(self)
        # self.create_attribute(ATTR_STEPS, default_value=0, default_type=np.int64, set_function=self._move_absolute)
        # self.create_attribute(ATTR_CLOSE_LOOP_UNIT, display=False)
        # self.create_attribute(ATTR_CLOSE_LOOP_FACTOR, default_value=[1, 1], default_type=TYPE_LIST, display=False)
        # self.create_attribute(ATTR_MOVE_METHOD, default_value=CLOSE_LOOP, default_type=[OPEN_LOOP, CLOSE_LOOP],
        #                       set_function=self.set_move_method)

    # def set_move_method(self, value):
    #     if value == OPEN_LOOP:
    #         self.enable_open_loop()
    #     elif value == CLOSE_LOOP:
    #         self.enable_close_loop()
    #
    # def enable_close_loop(self):
    #     if self.position_attribute_copy != None:
    #         self.set_attribute((ATTR_POSITION, UNIT), self.position_attribute_copy[UNIT])
    #         self.set_attribute((ATTR_POSITION, OFFSET), self.position_attribute_copy[OFFSET])
    #         self.set_attribute((ATTR_POSITION, FACTOR), self.position_attribute_copy[FACTOR])
    #         self.position_attribute_copy = None
    #
    # def enable_open_loop(self):
    #     self.position_attribute_copy = self[ATTR_POSITION].attribute_copy()
    #     default_unit = self.get_value(ATTR_CLOSE_LOOP_UNIT)
    #     self.set_attribute((ATTR_POSITION, UNIT), default_unit if default_unit != None else self.position_attribute_copy[UNIT])
    #     self.set_attribute((ATTR_POSITION, OFFSET), 0)
    #     self.set_attribute((ATTR_POSITION, FACTOR), 1)

    # def _move_absolute(self):
    #     raise NotImplementedError

    def command(self, command, callback=None, with_token=False, returning=True):
        return self.device.command(command, callback, with_token, returning)

    def subject_update(self, key, value, subject):
        if key == ATTR_STATUS:
            if value in READY_DEVICE_STATUSES:
                self.handle_configuration()
            else:
                self.configured = False
                self.set_status(value)

    def poll_command(self, command, interval):
        self.device.poll_command(command, interval)

    def remove_poll_command(self, command, interval):
        self.device.remove_poll_command(command, interval)

    def handle_configuration(self):
        raise NotImplementedError(u"Must be implemented in subclass")

    def disconnect(self):
        self.stop_polling()
        self.configured = False
        self.device.detach_observer(self)
        self.set_status(STATUS_DISCONNECTED)

    def reconnect(self, *args):
        self.device.attach_observer(self)
        self.handle_configuration()
