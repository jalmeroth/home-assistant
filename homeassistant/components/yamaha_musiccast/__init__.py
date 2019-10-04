"""The yamaha_musiccast component."""
import logging

import voluptuous as vol

from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.helpers import config_validation as cv

from .const import ATTR_MASTER, DOMAIN, SERVICE_JOIN, SERVICE_UNJOIN

SERVICE_SCHEMA = vol.Schema({vol.Optional(ATTR_ENTITY_ID): cv.entity_ids})

JOIN_SERVICE_SCHEMA = SERVICE_SCHEMA.extend({vol.Required(ATTR_MASTER): cv.entity_id})

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Handle service configuration."""

    def service_handle(service):
        """Handle services."""
        _LOGGER.debug("service_handle from id: %s", service.data.get(ATTR_ENTITY_ID))
        master_id = service.data.get(ATTR_MASTER)  # holds id of group master or None
        entity_ids = service.data.get(ATTR_ENTITY_ID)  # holds ids of group clients

        from pymusiccast.dist import DistGroup

        if service.service == SERVICE_JOIN:
            _LOGGER.debug("**JOIN** entities: %s on %s", entity_ids, master_id)
            DistGroup.join_add(master_id, entity_ids, hass)

        elif service.service == SERVICE_UNJOIN:
            _LOGGER.debug("**UNJOIN** entities: %s", entity_ids)
            DistGroup.unjoin(entity_ids, hass)

    hass.services.register(
        DOMAIN, SERVICE_JOIN, service_handle, schema=JOIN_SERVICE_SCHEMA
    )
    hass.services.register(
        DOMAIN, SERVICE_UNJOIN, service_handle, schema=SERVICE_SCHEMA
    )

    return True
