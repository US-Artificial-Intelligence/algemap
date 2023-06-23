from abc import ABC, abstractmethod
import os
import random
import csv
import json
from typing import Tuple, List
import shlex

class Template(ABC):
    @abstractmethod
    def generate(self, *args) -> List[Tuple[str, dict]]:
        pass


# the args are the names of the file(s) inside the variables folder, minus the .csv
# Reads CSV cells as though they were JSON
# If a row has only one element, it is not a list
def sample_from(*args):
    all_rows = []
    for arg in args:
        arg = arg + ".txt"
        path = os.path.join("variables", arg)
        with open(path, 'r') as f:
            rows = f.read().rstrip().split("\n")
            row = random.choice(rows)
            row = shlex.split(row, posix=True)
            row = [json.loads("\"" + x.replace("\"", "\\\"") + "\"") for x in row]
            if len(row) == 1:
                row = row[0]
            all_rows.append(row)
    return random.choice(all_rows)

def _power_law(x_min=1, a=1.2):
    # used chatGPT to find the inverse CDF for a power law distribution
    y = random.random()
    return ((1 - y) ** (1/(1 - a))) * x_min

def sample_small_int(dist="power", dist_args={}):
    if dist == "power":
        x = _power_law(**dist_args)
        return int(x)
    else:
        raise NotImplementedError(f"Unknown distribution value \"{dist}\"")
