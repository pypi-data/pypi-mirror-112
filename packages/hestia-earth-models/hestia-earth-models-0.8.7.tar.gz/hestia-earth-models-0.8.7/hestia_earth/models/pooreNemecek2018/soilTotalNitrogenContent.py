from hestia_earth.schema import MeasurementStatsDefinition
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_average

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils import is_from_model
from hestia_earth.models.utils.measurement import _new_measurement
from . import MODEL

TERM_ID = 'soilTotalNitrogenContent'
BIBLIO_TITLE = 'Reducing food’s environmental impacts through producers and consumers'


def _measurement(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    measurement = _new_measurement(TERM_ID, MODEL, BIBLIO_TITLE)
    measurement['value'] = [value]
    measurement['depthUpper'] = 0
    measurement['depthLower'] = 50
    measurement['statsDefinition'] = MeasurementStatsDefinition.MODELLED.value
    return measurement


def _run(carbon_content: float):
    value = 0.0000601 * (carbon_content / 100 * 5000 * 1300) / 11 * 1000
    return [_measurement(value)]


def _should_run(site: dict):
    carbon_content = find_term_match(site.get('measurements', []), 'soilOrganicCarbonContent')
    carbon_content_value = carbon_content.get('value', [])

    debugRequirements(model=MODEL, term=TERM_ID,
                      carbon_content_value=carbon_content_value)

    should_run = not is_from_model(carbon_content) and len(carbon_content_value) > 0
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, list_average(carbon_content_value)


def run(site: dict):
    should_run, carbon_content = _should_run(site)
    return _run(carbon_content) if should_run else []
