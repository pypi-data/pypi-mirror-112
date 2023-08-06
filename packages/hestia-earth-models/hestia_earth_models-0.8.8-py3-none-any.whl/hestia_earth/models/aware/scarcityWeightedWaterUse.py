from hestia_earth.schema import IndicatorStatsDefinition, SiteSiteType
from hestia_earth.utils.lookup import download_lookup, _get_single_table_value, column_name
from hestia_earth.utils.tools import safe_parse_float
from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_site
from . import MODEL
from .freshwaterWithdrawals import TERM_ID as ERU_TERM_ID

TERM_ID = 'scarcityWeightedWaterUse'
AWARE_KEY = 'awareWaterBasinId'
IRRIGATED_SITE_TYPES = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value
]


def _indicator(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    indicator['statsDefinition'] = IndicatorStatsDefinition.MODELLED.value
    return indicator


def _get_annual_characterization_factor(impact_assessment: dict):
    site = get_site(impact_assessment)
    aware_value = site.get(AWARE_KEY)
    lookup_col = 'YR_IRRI' if site.get('siteType') in IRRIGATED_SITE_TYPES else 'YR_NONIRRI'
    return safe_parse_float(
        _get_single_table_value(
            download_lookup(f"{AWARE_KEY}.csv", True), column_name(AWARE_KEY), int(aware_value), column_name(lookup_col)
        ), None
    ) if aware_value else None


def _run(fresh_water: float, awarecf: float):
    value = fresh_water * awarecf
    return [_indicator(value)]


def _should_run(impact_assessment: dict):
    # require fresh water emission resource use
    fresh_water = find_term_match(impact_assessment.get('emissionsResourceUse', []), ERU_TERM_ID).get('value')
    awarecf = _get_annual_characterization_factor(impact_assessment)

    debugRequirements(model=MODEL, term=TERM_ID,
                      fresh_water=fresh_water,
                      awarecf=awarecf)

    should_run = all([fresh_water, awarecf])
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, fresh_water, awarecf


def run(impact_assessment: dict):
    should_run, fresh_water, awarecf = _should_run(impact_assessment)
    return _run(fresh_water, awarecf) if should_run else []
