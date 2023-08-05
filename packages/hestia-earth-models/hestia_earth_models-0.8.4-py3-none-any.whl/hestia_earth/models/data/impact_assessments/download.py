import os
import json
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia, find_node

from hestia_earth.models.log import logger

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_NAME = 'Wernet et al (2016)'


def get_files(): return list(filter(lambda f: f.endswith('.jsonld'), os.listdir(CURRENT_DIR)))


def _save_assessment(id: str):
    data = download_hestia(id, SchemaType.IMPACTASSESSMENT)
    file_path = f"{CURRENT_DIR}/{id}.jsonld"
    logger.debug(f"saving {file_path}...")
    with open(file_path, 'w') as f:
        return json.dump(data, f, indent=2)


def _run():
    logger.info('Downloading Impacts...')

    nodes = find_node(SchemaType.IMPACTASSESSMENT, {'source.name.keyword': SOURCE_NAME}, 1000)
    nodes = [node.get('@id') for node in nodes]
    logger.debug('Found %s matching impacts', len(nodes))

    with ThreadPoolExecutor() as executor:
        executor.map(_save_assessment, nodes)

    logger.info('Impacts downloaded.')


def _should_run():
    should_run = len(get_files()) == 0
    logger.debug('Should download impacts: %s', should_run)
    return should_run


def run(): return _run() if _should_run() else None
