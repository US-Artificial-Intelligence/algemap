from abc import ABC, abstractmethod
import os
import random

class Template(ABC):

    @abstractmethod
    def generate(self, *args):
        pass

# the args are the names of the file(s) inside the variables folder, minus the .txt
def sample_from(*args):

    all_lines = []
    for arg in args:
        arg = arg + ".txt"
        path = os.path.join("variables", arg)
        with open(path, "r") as fhand:
            lines = fhand.read().splitlines()
            all_lines.extend(lines)
    return random.choice(all_lines)

    