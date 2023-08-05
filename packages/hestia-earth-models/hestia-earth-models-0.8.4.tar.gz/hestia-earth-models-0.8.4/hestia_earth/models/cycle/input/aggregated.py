import math
from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import search
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.tools import non_empty_list, safe_parse_date

from hestia_earth.models.log import logger
from hestia_earth.models.utils.cycle import is_organic, is_irrigated
MODEL = 'aggregated'
MODEL_KEY = 'impactAssessment'
HESTIA_BIBLIO_TITLE = 'Hestia: A new data platform for storing and analysing data on the productivity \
and sustainability of agriculture'


def _name_suffix(cycle: dict):
    return '-'.join(non_empty_list([
        'Organic' if is_organic(cycle) else 'Conventional',
        'Irrigated' if is_irrigated(cycle) else 'Non Irrigated'
    ]))


def _end_date(end_date: str):
    year = safe_parse_date(end_date).year
    return round((math.floor(year / 10) + 1) * 10)


def _find_closest_impact(cycle: dict, country: dict, end_date: str, input: dict):
    query = {
        'bool': {
            'must': [
                {'match': {'@type': SchemaType.IMPACTASSESSMENT.value}},
                {'match': {'source.bibliography.title.keyword': HESTIA_BIBLIO_TITLE}},
                {'match': {'product.name.keyword': input.get('term', {}).get('name')}},
                {
                    'bool': {
                        # either get with exact country, or default to global
                        'should': [
                            {'match': {'country.name.keyword': {'query': country.get('name'), 'boost': 1000}}},
                            {'match': {'country.name.keyword': {'query': 'World', 'boost': 1}}}
                        ],
                        'minimum_should_match': 1
                    }
                }
            ],
            'should': [
                {'match': {'name': _name_suffix(cycle)}},
                {'match': {'endDate': _end_date(end_date)}}
            ]
        }
    }
    results = search(query)
    result = results[0] if len(results) > 0 else {}
    logger.debug('found aggregated impact for term=%s: %s', input.get('term', {}).get('@id'), result.get('@id'))
    return result


def _run(cycle: dict, inputs: list, country: dict, end_date: str):
    inputs = [
        {**i, MODEL_KEY: linked_node(_find_closest_impact(cycle, country, end_date, i))} for i in inputs
    ]
    return list(filter(lambda i: i.get(MODEL_KEY).get('@id') is not None, inputs))


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    country = cycle.get('site', {}).get('country')
    # do not override inputs that already have an impactAssessment
    inputs = [i for i in cycle.get('inputs', []) if not i.get(MODEL_KEY)]

    should_run = end_date is not None and country is not None and len(inputs) > 0
    logger.info('model=%s, should_run=%s', MODEL, should_run)
    return should_run, inputs, country, end_date


def run(cycle: dict):
    should_run, inputs, country, end_date = _should_run(cycle)
    return _run(cycle, inputs, country, end_date) if should_run else []
