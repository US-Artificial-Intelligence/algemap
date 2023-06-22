from abc import ABC, abstractmethod
import os
import random
import csv
import json


class Template(ABC):

    @abstractmethod
    def generate(self, *args):
        pass

# the args are the names of the file(s) inside the variables folder, minus the .csv
def sample_from(*args):
    all_rows = []
    for arg in args:
        arg = arg + ".csv"
        path = os.path.join("variables", arg)
        with open(path, 'r') as f:
            rows = f.read().rstrip().split("\n")
            row = random.choice(rows).split(",")
            row = [json.loads(x) for x in row]
            all_rows.append(row)
    return random.choice(all_rows)

# uniformly random
# returns question prefix, answer prefix
def sample_qa_prefixes():
    options = [
        # Simple Question / Answer
        ("Q: ", "A: "),
        ("Question: ", "Answer: "),
        ("Question\n", "Answer\n"),
        ("Question\n\n", "Answer\n\n"),
        ("**Question**: ", "**Answer**: "),
        ("**Q**: ", "**A**: "),
        ("**Q:** ", "**A:** "),
        ("\n\n\"\"\"QUESTION\"\"\"\n\n", "\n\"\"\"ANSWER\"\"\"\n\n"),
        # Command style
        ("Please respond to the following question.\n\n", "---\n\nAnswer:"),
        ("Answer the following:\n\n", "\nResponse:"),
        ("The following is a question from a user. Please respond clearly and succinctly.", "Your response: ")
    ]
    return random.choice(options)
    