import json
from tests.utils import fixtures_path

from hestia_earth.models.cycle.input.ecoinventV3 import MODEL, run

class_path = f"hestia_earth.models.cycle.input.{MODEL}"
fixtures_folder = f"{fixtures_path}/cycle/input/{MODEL}"


def test_run():
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(cycle)
    assert result == expected
