from enum import Enum
from hestia_earth.schema import MeasurementStatsDefinition
from hestia_earth.utils.tools import list_average
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.measurement import _new_measurement

from . import MODEL

TERM_ID = 'netPrimaryProduction'


class TemperatureLevel(Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


NPP_Aqua = {TemperatureLevel.LOW: 2, TemperatureLevel.MEDIUM: 4, TemperatureLevel.HIGH: 5}

NPP_FROM_TEMP = {
    TemperatureLevel.LOW: lambda temp: temp < 15,
    TemperatureLevel.MEDIUM: lambda temp: 15 < temp < 23.5,
    TemperatureLevel.HIGH: lambda _temp: True
}


def _measurement(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    measurement = _new_measurement(TERM_ID, MODEL)
    measurement['value'] = [value]
    measurement['statsDefinition'] = MeasurementStatsDefinition.MODELLED.value
    return measurement


def _npp(temp: float):
    npp_key = next((key for key in NPP_FROM_TEMP if NPP_FROM_TEMP[key](temp)), None)
    return NPP_Aqua[npp_key]


def _run(temp: float):
    value = _npp(temp)
    return [_measurement(value)]


def _should_run(site: dict):
    measurements = site.get('measurements', [])
    temperature = list_average(find_term_match(measurements, 'temperatureAnnual').get('value', []))

    debugRequirements(model=MODEL, term=TERM_ID,
                      temperature=temperature)

    should_run = temperature > 0
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, temperature


def run(site: dict):
    should_run, temp = _should_run(site)
    return _run(temp) if should_run else []
