from .utils import Template, sample_from, sample_small_int
import random
import tiktoken

"""

Sequences of the form:

1, 2, 4, 8, 16

(2^i)

Or

5, 9, 17, 33

(2^(i+2)+1)

for example.

"""

class Sequence(Template):
    def generate(self, max_sequence_length=10, min_sequence_length=4):
        seq_generator = self.get_func()

    def get_func(self):
        return lambda x: x**2.
