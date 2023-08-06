from hestia_earth.schema import EmissionMethodTier, EmissionStatsDefinition
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import debugRequirements, logger
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.product import total_excreta_tan
from hestia_earth.models.utils.practice import is_model_enabled
from . import MODEL

TERM_ID = 'nh3ToAirAquaculturePonds'
EF_Aqua = {'TAN_NH3N': 0.3, 'MAX_NH3N': 0.05}


def _emission(value: float):
    logger.info('model=%s, term=%s, value=%s', MODEL, TERM_ID, value)
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = EmissionMethodTier.TIER_1.value
    emission['statsDefinition'] = EmissionStatsDefinition.MODELLED.value
    return emission


def _run(excr_tan: float, yield_of_target_species: float, has_slow_flowing: bool):
    tan_value = excr_tan * EF_Aqua['TAN_NH3N']
    value = min([tan_value, EF_Aqua['MAX_NH3N'] * 365 / yield_of_target_species]) if has_slow_flowing else tan_value
    return [_emission(value)]


def _should_run(cycle: dict):
    practices = cycle.get('practices', [])
    first_practice = practices[0] if len(practices) > 0 else None
    model_enabled = is_model_enabled(MODEL, TERM_ID, first_practice)
    products = cycle.get('products', [])
    excr_tan = total_excreta_tan(products)
    yield_of_target_species = safe_parse_float(find_term_match(practices, 'yieldOfTargetSpecies').get('value'))

    measurements = cycle.get('site', {}).get('measurements', [])
    has_slow_flowing = find_term_match(measurements, 'slowFlowingWater', None) is not None

    debugRequirements(model=MODEL, term=TERM_ID,
                      model_enabled=model_enabled,
                      excr_tan=excr_tan,
                      yield_of_target_species=yield_of_target_species,
                      has_slow_flowing=has_slow_flowing)

    should_run = model_enabled and excr_tan > 0 and (not has_slow_flowing or yield_of_target_species > 0)
    logger.info('model=%s, term=%s, should_run=%s', MODEL, TERM_ID, should_run)
    return should_run, excr_tan, yield_of_target_species, has_slow_flowing


def run(cycle: dict):
    should_run, excr_tan, yield_of_target_species, has_slow_flowing = _should_run(cycle)
    return _run(excr_tan, yield_of_target_species, has_slow_flowing) if should_run else []
