from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.stehfestBouwman2006.n2OToAirAllOrigins import TERM_ID, run, _get_value, _should_run

class_path = f"hestia_earth.models.stehfestBouwman2006.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/stehfestBouwman2006/{TERM_ID}"


@patch(f"{class_path}.valid_site_type", return_value=True)
@patch(f"{class_path}.most_relevant_measurement_value", return_value=[])
def test_should_run(mock_most_relevant_measurement_value, _m):
    # no measurements => no run
    cycle = {}
    should_run, *args = _should_run(cycle)
    assert not should_run

    # with measurements => no run
    mock_most_relevant_measurement_value.return_value = [10]
    should_run, *args = _should_run(cycle)
    assert not should_run

    # with kg N inputs => no run
    cycle['inputs'] = [{
        'term': {
            'units': 'kg N'
        },
        'value': [100]
    }]
    should_run, *args = _should_run(cycle)
    assert not should_run

    # with primary product => run
    cycle['products'] = [{
        'term': {
            '@id': 'cerealsGrain'
        },
        'primary': True
    }]
    should_run, *args = _should_run(cycle)
    assert should_run is True


def test_get_value():
    content_list_of_items = [[8], [81], [0.58], [5.7], '2', 'None']
    N_total = 100
    assert _get_value(content_list_of_items, N_total) == 3.6132443350109704


@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
def test_run(*args):
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
