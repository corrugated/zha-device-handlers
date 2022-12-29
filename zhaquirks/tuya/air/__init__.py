"""Tuya Air sensors."""

from typing import Dict

import zigpy.types as t
from zigpy.zcl.clusters.measurement import (
    CarbonDioxideConcentration,
    FormaldehydeConcentration,
    PM25,
    RelativeHumidity,
    TemperatureMeasurement,
)

from zhaquirks.tuya import DPToAttributeMapping, TuyaLocalCluster, TuyaNewManufCluster


class TuyaAirQualityVOC(TuyaLocalCluster):
    """Tuya VOC level cluster."""

    cluster_id = 0x042E
    name = "VOC Level"
    ep_attribute = "voc_level"

    attributes = {
        0x0000: ("measured_value", t.Single),  # fraction of 1 (one)
        0x0001: ("min_measured_value", t.Single),
        0x0002: ("max_measured_value", t.Single),
        0x0003: ("tolerance", t.Single),
    }

    server_commands = {}
    client_commands = {}


class TuyaAirQualityTemperature(TemperatureMeasurement, TuyaLocalCluster):
    """Tuya temperature measurement."""


class TuyaAirQualityHumidity(RelativeHumidity, TuyaLocalCluster):
    """Tuya relative humidity measurement."""


class TuyaAirQualityCO2(CarbonDioxideConcentration, TuyaLocalCluster):
    """Tuya Carbon Dioxide concentration measurement."""


class TuyaAirQualityFormaldehyde(FormaldehydeConcentration, TuyaLocalCluster):
    """Tuya Formaldehyde concentration measurement."""


class TuyaAirQualityPM25(PM25, TuyaLocalCluster):
    """Tuya PM25 measurement."""


class TuyaCO2ManufCluster(TuyaNewManufCluster):
    """Tuya with Air quality data points."""

    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        2: DPToAttributeMapping(
            TuyaAirQualityCO2.ep_attribute,
            "measured_value",
            lambda x: x * 1e-6,
        ),
        18: DPToAttributeMapping(
            TuyaAirQualityTemperature.ep_attribute, "measured_value", lambda x: x * 10
        ),
        19: DPToAttributeMapping(
            TuyaAirQualityHumidity.ep_attribute, "measured_value", lambda x: x * 10
        ),
        21: DPToAttributeMapping(
            TuyaAirQualityVOC.ep_attribute, "measured_value", lambda x: x * 1e-6
        ),
        22: DPToAttributeMapping(
            TuyaAirQualityFormaldehyde.ep_attribute,
            "measured_value",
            lambda x: x * 1e-6,
        ),
    }

    data_point_handlers = {
        2: "_dp_2_attr_update",
        18: "_dp_2_attr_update",
        19: "_dp_2_attr_update",
        21: "_dp_2_attr_update",
        22: "_dp_2_attr_update",
    }


class TuyaAirHousekeeperManufCluster(TuyaNewManufCluster):
    """Tuya intelligent air housekeeper (6in1) device data points."""

    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        2: DPToAttributeMapping(
            TuyaAirQualityPM25.ep_attribute,
            "measured_value",
            # The sensor sometimes gives garbage values 0xAAAB, 0xAAAC and
            # simiar.  Filter out all values above or equal 0xAA00, as these
            # are outside of the measurement range anyhow.
            lambda x: None if x >= 0xAA00 else x,
        ),
        18: DPToAttributeMapping(
            TuyaAirQualityTemperature.ep_attribute,
            "measured_value",
            lambda x: x * 10,
        ),
        19: DPToAttributeMapping(
            TuyaAirQualityHumidity.ep_attribute,
            "measured_value",
            lambda x: x * 10,
        ),
        20: DPToAttributeMapping(
            TuyaAirQualityFormaldehyde.ep_attribute,
            "measured_value",
            lambda x: x,
        ),
        21: DPToAttributeMapping(
            TuyaAirQualityVOC.ep_attribute,
            "measured_value",
            lambda x: x,
        ),
        22: DPToAttributeMapping(
            TuyaAirQualityCO2.ep_attribute,
            "measured_value",
            lambda x: x * 1e-6,
        ),
    }

    data_point_handlers = {
        2: "_dp_2_attr_update",
        18: "_dp_2_attr_update",
        19: "_dp_2_attr_update",
        20: "_dp_2_attr_update",
        21: "_dp_2_attr_update",
        22: "_dp_2_attr_update",
    }
