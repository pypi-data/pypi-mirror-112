from hestia_earth.schema import PracticeStatsDefinition
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logger
from hestia_earth.models.utils.practice import _new_practice
from hestia_earth.models.utils.cycle import valid_site_type
from hestia_earth.models.utils import _filter_list_term_unit
from hestia_earth.models.utils.blank_node import get_total_value, get_total_value_converted
from .. import MODEL
from . import feedConversionRatioCarbon
from . import feedConversionRatioDryMatter
from . import feedConversionRatioEnergy
from . import feedConversionRatioFedWeight
from . import feedConversionRatioNitrogen

MODELS = [
    feedConversionRatioCarbon,
    feedConversionRatioDryMatter,
    feedConversionRatioEnergy,
    feedConversionRatioFedWeight,
    feedConversionRatioNitrogen
]


def _practice(term_id: str, value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, term_id, value)
    practice = _new_practice(term_id)
    practice['value'] = value
    practice['statsDefinition'] = PracticeStatsDefinition.MODELLED.value
    return practice


def _run(cycle: dict, kg_liveweight: float):
    return [_practice(model.TERM_ID, model.run(cycle) / kg_liveweight) for model in MODELS]


def _calculate_liveweight_produced(cycle: dict):
    products = cycle.get('products', [])
    kg_liveweight = _filter_list_term_unit(products, 'kg liveweight')
    kg_carcass = _filter_list_term_unit(products, 'kg carcass weight')
    return list_sum(
        get_total_value(kg_liveweight) +
        get_total_value_converted(kg_carcass, 'processingConversionLiveweightToCarcassWeight', False)
    )


def _should_run(cycle: dict):
    kg_liveweight = _calculate_liveweight_produced(cycle)
    logger.debug('kg liveweight=%s', kg_liveweight)

    should_run = valid_site_type(cycle) and kg_liveweight > 0
    logger.info('model=%s, term=%s, should_run=%s', MODEL, 'feedConversionRatio', should_run)
    return should_run, kg_liveweight


def run(cycle: dict):
    should_run, kg_liveweight = _should_run(cycle)
    return _run(cycle, kg_liveweight) if should_run else []
