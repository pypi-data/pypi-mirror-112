from hestia_earth.schema import CycleFunctionalUnitMeasure, IndicatorStatsDefinition

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, get_site
from hestia_earth.models.utils.cycle import calculate_land_occupation
from . import MODEL

TERM_ID = 'landOccupation'


def _indicator(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _run(impact_assessment: dict, product: dict):
    cycle = impact_assessment.get('cycle', {})
    site = get_site(impact_assessment)
    value = calculate_land_occupation(cycle, site, product)
    return [_indicator(value)] if value else []


def _should_run(impact_assessment: dict):
    functionalUnitMeasure = impact_assessment.get('cycle', {}).get('functionalUnitMeasure')
    product = get_product(impact_assessment)

    debugRequirements(model=MODEL, term=TERM_ID,
                      functionalUnitMeasure=functionalUnitMeasure)

    should_run = product is not None and functionalUnitMeasure == CycleFunctionalUnitMeasure._1_HA.value
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, product


def run(impact_assessment: dict):
    should_run, product = _should_run(impact_assessment)
    return _run(impact_assessment, product) if should_run else []
