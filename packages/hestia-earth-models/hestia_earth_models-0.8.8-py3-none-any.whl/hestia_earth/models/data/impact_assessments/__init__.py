import os
import sys
import json

from .download import run, get_files

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.append(CURRENT_DIR)


def load_impacts():
    # download all impacts first if not done yet
    run()

    files = get_files()
    impacts = []
    for filename in files:
        with open(os.path.join(CURRENT_DIR, filename), 'r') as file:
            impacts.append(json.load(file))
    return impacts
