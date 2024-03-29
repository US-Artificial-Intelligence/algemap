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
    def generate(self, max_sequence_length=10, min_sequence_length=4, n=10, show_rule=True, show_instructions=False, show_rule_after=False) -> List[Tuple[str, dict]]:
        results = [self.gen_one(max_sequence_length=max_sequence_length, min_sequence_length=min_sequence_length, show_rule=show_rule, show_instructions=show_instructions, show_rule_after=show_rule_after) for _ in range(n)]
        return results

    def gen_one(self, max_sequence_length=10, min_sequence_length=4, show_rule=False, show_instructions=False, show_rule_after=True):
        seq_generator, representation = self.get_func()
        seq_len = random.randrange(min_sequence_length, max_sequence_length+1)
        sequence = [str(int(seq_generator(i))) for i in range(seq_len)]

        delimeter: str = sample_from("seq_delimeters")

        txt = ""
        if show_instructions:
            txt += "The following sequence is arithmetically generated by computer according to a rule.\n\n"
        if show_rule and not show_rule_after:
            txt += f"The rule: {representation}\n\n"

        txt += delimeter.join(sequence)

        if show_rule and show_rule_after:
            txt += f"The rule: {representation}\n\n"

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

        """
        Variables with name _ have distribution of _
        ----
        c --> integers 2, 3, or 4 (uniformly random)
        b --> integers 2, 3, or 4 (uniformly random)
        a --> integers between 0 and 10 (uniformly random)
        k --> integers between 2 and 50 (uniformly random)
        o --> integers between 0 and 100 (50% 0, otherwise uniformly random)

        i's are index values.
        """

        forms = [
            "{c}^{i}+{o}",
            "{c}^({i}+{b})+{o}",
            "{k}*{i}+{o}",
            "{i}^{c}+{o}",
            "{k}*({i}+{a})",
            "{c}*{b}^{i}",
            "{c}*{b}^{i}+{o}",
            "{i}+{o}+{k}",
            "{i}+{o}*{k}"
        ]

        def string_to_func(string):
            # replace '^' with '**'
            string = string.replace('^', '**')
            def func(x):
                return eval(string)
            return func
        
        c = random.randint(2, 4)
        b = random.randint(2, 4)
        a = random.randint(0, 10)
        k = random.randint(2, 50)
        o = 0 if random.random() < .5 else random.randint(1, 100)
        str_func = random.choice(forms)
        str_func = str_func.format(c=c, b=b, a=a, k=k, o=o, i="x")
        return string_to_func(str_func), str_func
