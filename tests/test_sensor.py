"""Test NWS Alerts Sensors"""

import pytest
from homeassistant.helpers import entity_registry as er
from homeassistant.util import slugify
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.nws_alerts.const import DOMAIN
from tests.const import CONFIG_DATA, CONFIG_DATA_2, CONFIG_DATA_BAD

pytestmark = pytest.mark.asyncio

NWS_SENSOR = "sensor.nws_alerts"
NWS_SENSOR_2 = "sensor.nws_alerts_yaml"


async def test_sensor(hass, mock_api):
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="NWS Alerts",
        data=CONFIG_DATA,
    )

    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert "nws_alerts" in hass.config.components
    state = hass.states.get(NWS_SENSOR)
    assert state
    assert state.state == "2"
    assert state.attributes["alert0"] == {
        "id": "cbc5f830-921d-10c7-b447-e9bc1b744965",
        "headline": "OZONE HIGH POLLUTION ADVISORY FOR MARICOPA COUNTY INCLUDING THE PHOENIX METRO AREA THROUGH FRIDAY",
        "url": "https://api.weather.gov/alerts/urn:oid:2.49.0.1.840.0.32b8fe5b1e8094248fdbb7a32619581ec4e1df14.001.1",
        "type": "Alert",
        "status": "Actual",
        "description": "AQAPSR\n\nThe Arizona Department of Environmental Quality (ADEQ) has issued an\nOzone High Pollution Advisory for the Phoenix Metro Area through\nFriday.\n\nThis means that forecast weather conditions combined with existing\nozone levels are expected to result in local maximum 8-hour ozone\nconcentrations that pose a health risk. Adverse health effects\nincrease as air quality deteriorates.\n\nOzone is an air contaminant which can cause breathing difficulties\nfor children, older adults, as well as persons with respiratory\nproblems. A decrease in physical activity is recommended.\n\nYou are urged to car pool, telecommute or use mass transit.\nThe use of gasoline-powered equipment should be reduced or done late\nin the day.\n\nFor details on this High Pollution Advisory, visit the ADEQ internet\nsite at www.azdeq.gov/forecast/phoenix or call 602-771-2300.",
        "instruction": None,
        "severity": "Unknown",
        "certainty": "Unknown",
        "onset": "2024-07-18T08:13:00-07:00",
        "expires": "2024-07-19T21:00:00-07:00",
        "display_desc": "\n>\nHeadline: OZONE HIGH POLLUTION ADVISORY FOR MARICOPA COUNTY INCLUDING THE PHOENIX METRO AREA THROUGH FRIDAY\nStatus: Actual\nMessage Type: Alert\nSeverity: Unknown\nCertainty: Unknown\nOnset: 2024-07-18T08:13:00-07:00\nExpires: 2024-07-19T21:00:00-07:00\nDescription: AQAPSR\n\nThe Arizona Department of Environmental Quality (ADEQ) has issued an\nOzone High Pollution Advisory for the Phoenix Metro Area through\nFriday.\n\nThis means that forecast weather conditions combined with existing\nozone levels are expected to result in local maximum 8-hour ozone\nconcentrations that pose a health risk. Adverse health effects\nincrease as air quality deteriorates.\n\nOzone is an air contaminant which can cause breathing difficulties\nfor children, older adults, as well as persons with respiratory\nproblems. A decrease in physical activity is recommended.\n\nYou are urged to car pool, telecommute or use mass transit.\nThe use of gasoline-powered equipment should be reduced or done late\nin the day.\n\nFor details on this High Pollution Advisory, visit the ADEQ internet\nsite at www.azdeq.gov/forecast/phoenix or call 602-771-2300.\nInstruction: None",
    }
    entity_registry = er.async_get(hass)
    entity = entity_registry.async_get(NWS_SENSOR)
    assert entity.unique_id == f"{slugify(entry.title)}_{entry.entry_id}"

    entry = MockConfigEntry(
        domain=DOMAIN,
        title="NWS Alerts YAML",
        data=CONFIG_DATA_2,
    )

    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert "nws_alerts" in hass.config.components
    state = hass.states.get(NWS_SENSOR_2)
    assert state
    entity_registry = er.async_get(hass)
    entity = entity_registry.async_get(NWS_SENSOR_2)
    assert entity.unique_id == f"{slugify(entry.title)}_{entry.entry_id}"
