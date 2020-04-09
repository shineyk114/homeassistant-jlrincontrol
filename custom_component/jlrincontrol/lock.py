"""Support for JLR InControl Locks."""
import logging

# from homeassistant.const import STATE_OFF, UNIT_PERCENTAGE
from homeassistant.components.lock import LockDevice
from . import JLREntity, DOMAIN
from .const import DATA_ATTRS_DOOR_POSITION, DATA_ATTRS_DOOR_STATUS


_LOGGER = logging.getLogger(__name__)
DATA_KEY = DOMAIN


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    data = hass.data[DOMAIN]
    devices = []
    _LOGGER.debug("Loading locks")

    devices.append(JLRLock(data))

    async_add_entities(devices, True)


class JLRLock(JLREntity, LockDevice):
    def __init__(self, data):
        super().__init__(data, "vehicle")
        self.data = data
        _LOGGER.debug(
            "Loading vehicle lock for {}".format(
                self.data.attributes.get("registrationNumber")
            )
        )
        self._name = self.data.attributes.get("nickname") + " Doors"

    @property
    def is_locked(self):
        """Return true if lock is locked."""
        _LOGGER.debug("Getting state of vehicle lock")
        return self.data.status.get("DOOR_IS_ALL_DOORS_LOCKED") == "TRUE"

    def lock(self, **kwargs):
        """Lock the car."""
        _LOGGER.debug("Locking vehicle")
        # self.instrument.lock()

    def unlock(self, **kwargs):
        """Unlock the car."""
        _LOGGER.debug("Unlocking vehicle")
        # self.instrument.unlock()

    @property
    def icon(self):
        return "mdi:car-key"

    @property
    def device_state_attributes(self):
        s = self.data.status
        attrs = {}
        for k, v in DATA_ATTRS_DOOR_STATUS.items():
            attrs[k.title() + " Status"] = s.get(v).title()

        for k, v in DATA_ATTRS_DOOR_POSITION.items():
            attrs[k.title() + " Position"] = s.get(v).title()

        return attrs
