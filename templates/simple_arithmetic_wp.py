from .utils import Template, sample_from, sample_small_int
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
        num1 = sample_small_int()
        num2 = sample_small_int()
        is_boy = random.random() < .5
        if is_boy:
            name = sample_from("boy_names")
        else:
            name = sample_from("girl_names")
        singular, plural = sample_from("noun_pairs")
        if num1 == 1:
            noun = singular
        else:
            noun = plural
        
        cap_pronoun, pronoun = ("He", "he") if is_boy else ("She", "she")
        q_prefix, a_prefix = sample_from("qa_prefixes")

        add_verb = sample_from("add_verbs")

        repeat_noun = "" if random.random() < .5 else " " + plural
        say_now = "" if random.random() < .5 else " now"
        last_word = plural if random.random() < .5 else "of them"

        answer = num1 + num2

        add = f"""{q_prefix}{name} had {num1} {noun}. {cap_pronoun} {add_verb} {num2} more. How many{repeat_noun} does {pronoun} have now?
{a_prefix}{cap_pronoun}{say_now} has {answer} {last_word}."""
        
        metadata = {
            'len': len(add),
            'answer_start_char': add.find(str(answer)),
            'answer_len': len(str(answer))
        }

        return add, metadata
