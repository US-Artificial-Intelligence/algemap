from .utils import Template, sample_from, sample_small_int
import random
import tiktoken
from typing import Tuple, List

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
    def generate(self, max_sequence_length=10, min_sequence_length=4, n=10) -> List[Tuple[str, dict]]:
        return [self.gen_one() for _ in range(10)]

    def gen_one(self, max_sequence_length=10, min_sequence_length=4):
        seq_generator, representation = self.get_func()
        seq_len = random.randrange(min_sequence_length, max_sequence_length+1)
        sequence = [str(int(seq_generator(i))) for i in range(seq_len)]

        delimeter: str = sample_from("seq_delimeters")
        txt = delimeter.join(sequence)

        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(txt)

        metadata = {
            'char_len': len(txt),
            'rule': representation,
            'tokens': tokens,
            'tokenizer': "cl100k_base",
            'tokens_len': len(tokens),
            'data_type': 'arithmetic_sequence'
        }
            
        return txt, metadata

    def get_func(self):
        return lambda x: x**2., "x^2"
