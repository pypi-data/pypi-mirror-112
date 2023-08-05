from dateutil import parser
from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.tools import list_average

from . import _term_id, _include_methodModel, _include_source

# TODO verify those values
MAX_DEPTH = 1000
OLDEST_DATE = '1800'


def _new_measurement(term, model=None, biblio_title=None):
    node = {'@type': SchemaType.MEASUREMENT.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_methodModel(_include_source(node, biblio_title), model)


def measurement_value_average(measurement: dict): return list_average(measurement.get('value', [0]))


def _measurement_date(measurement: dict): return parser.isoparse(measurement.get('endDate', OLDEST_DATE))


def _distance(measurement: dict, date): return abs((_measurement_date(measurement) - date).days)


def _most_recent_measurements(measurements: list, date: str) -> list:
    closest_date = parser.isoparse(date)
    min_distance = min([_distance(m, closest_date) for m in measurements])
    return list(filter(lambda m: _distance(m, closest_date) == min_distance, measurements))


def _shallowest_measurement(measurements: list) -> dict:
    min_depth = min([m.get('depthUpper', MAX_DEPTH) for m in measurements])
    return next((m for m in measurements if m.get('depthUpper', MAX_DEPTH) == min_depth), {})


def most_relevant_measurement(measurements: list, term_id: str, date: str):
    filtered_measurements = [m for m in measurements if m.get('term', {}).get('@id') == term_id]
    return {} if len(filtered_measurements) == 0 \
        else _shallowest_measurement(_most_recent_measurements(filtered_measurements, date)) \
        if len(filtered_measurements) > 1 else filtered_measurements[0]


def most_relevant_measurement_value(measurements: list, term_id: str, date: str):
    return most_relevant_measurement(measurements, term_id, date).get('value', [])
