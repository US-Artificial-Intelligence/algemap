from .utils import Template, sample_from
import random

"""

Simple arithmetic word problems of the form:

Question: Sally had 5 apples. She gave away 2. How many apples does she have left?

Answer: 3 apples.

"""

class SimpleArithmeticWP(Template):
    def generate(self, *args):
        results = []
        for _ in range(10):
            results.append(self.addition())
        return results

    def addition(self):
        num1 = random.randrange(1, 100_000)
        num2 = random.randrange(1, 100_000)
        is_boy = random.random() < .5
        if is_boy:
            name = sample_from("boy_names")
        else:
            name = sample_from("girl_names")
        singular, plural = sample_from("noun_pairs").split(",")
        if num1 == 1:
            noun = singular
        else:
            noun = plural
        
        cap_pronoun, pronoun = ("He", "he") if is_boy else ("She", "she")
        q_prefix, a_prefix = ("Q:", "A:") if random.random() < .5 else ("Question:", "Answer:")

        add = f"""{q_prefix} {name} had {num1} {noun}. {cap_pronoun} gained {num2} more. How many does {pronoun} have now?
{a_prefix} {cap_pronoun} now has {num1 + num2} {plural}."""
        
        return add
