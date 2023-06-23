from .utils import Template, sample_from, sample_small_int
import random
import tiktoken

"""

Simple arithmetic word problems of the form:

Question: Sally had 5 apples. She gave away 2. How many apples does she have left?

Answer: 3 apples.

"""

class SimpleArithmeticWP(Template):
    def generate(self, simple_addition=5, simple_subtraction=5, multi_num=5):

        results = []
        for _ in range(simple_addition):
            results.append(self.simple_two_num(kind="addition"))
        for _ in range(simple_subtraction):
            results.append(self.simple_two_num(kind="subtraction"))
        for _ in range(multi_num):
            results.append(self.multi_num())
        return results

    def simple_two_num(self, kind):

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

        if kind == "addition":
            verb = sample_from("add_verbs")
            verb_follow_up = "" if random.random() < .5 else " more"
            answer = num1 + num2
        elif kind == "subtraction":
            verb = sample_from("sub_verbs")
            verb_follow_up = ""
            answer = num1 - num2
        else:
            raise NotImplementedError(f"Word problem type '{kind}' not recognized.")

        repeat_noun = "" if random.random() < .5 else " " + plural
        say_now = "" if random.random() < .5 else " now"
        last_word = plural if random.random() < .5 else "of them"

        add = f"""{q_prefix}{name} had {num1} {noun}. {cap_pronoun} {verb} {num2}{verb_follow_up}. How many{repeat_noun} does {pronoun} have now?
{a_prefix}{cap_pronoun}{say_now} has {answer} {last_word}."""
        
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(add)

        metadata = {
            'char_len': len(add),
            'answer_start_char': add.find(str(answer)),
            'answer_char_len': len(str(answer)),
            'tokens': tokens,
            'tokenizer': "cl100k_base",
            'tokens_len': len(tokens),
            "word_problem_type": kind,
            "shows_work": False,
            'data_type': 'simple_arithmetic_wp'
        }

        return add, metadata
    
    # Mixed addition and subtraction
    def multi_num(self, n=None, max_n=5):

        if n is None:
            n = random.randrange(2, max_n)
        
        nums = []
        operations = []
        answer = 0
        for i in range(n):
            if i == 0:
                nums.append(sample_small_int())
                answer += nums[-1]
            else:
                # addition
                if random.random() < .5:
                    operations.append("addition")
                    num = sample_small_int()
                    answer += num
                    nums.append(num)
                else:
                    operations.append("subtraction")
                    num = random.randrange(0, answer+1)
                    answer -= num
                    nums.append(num)
                    
        is_boy = random.random() < .5
        if is_boy:
            name = sample_from("boy_names")
        else:
            name = sample_from("girl_names")
        singular, plural = sample_from("noun_pairs")
        if nums[0] == 1:
            noun = singular
        else:
            noun = plural
        
        cap_pronoun, pronoun = ("He", "he") if is_boy else ("She", "she")
        q_prefix, a_prefix = sample_from("qa_prefixes")

        txt = f"{q_prefix}{name} had {nums[0]} {noun}. "

        for i in range(1, len(nums)):
            say_then = random.random() < .5
            if operations[i-1] == "addition":
                verb = sample_from("add_verbs")
                verb_follow_up = "" if random.random() < .5 else " more"
                txt += f"{'Then ' + pronoun if say_then else cap_pronoun} {verb} {nums[i]}{verb_follow_up}. "
            elif operations[i-1] == "subtraction":
                verb = sample_from("sub_verbs")
                txt += f"{'Then ' + pronoun if say_then else cap_pronoun} {verb} {nums[i]}. "
            else:
                raise NotImplementedError(f"Word problem type '{operations[i]}' not recognized.")
        
        last_word = plural if random.random() < .5 else "of them"
        repeat_noun = "" if random.random() < .5 else " " + plural
        say_now = "" if random.random() < .5 else " now"

        txt += f"How many{repeat_noun} does {pronoun} have now?\n{a_prefix}{cap_pronoun}{say_now} has {answer} {last_word}."""
        
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(txt)

        metadata = {
            'char_len': len(txt),
            'answer_start_char': txt.find(str(answer)),
            'answer_char_len': len(str(answer)),
            'tokens': tokens,
            'tokenizer': "cl100k_base",
            'tokens_len': len(tokens),
            "word_problem_type": 'mixed',
            "shows_work": False,
            'data_type': 'simple_arithmetic_wp'
        }

        return txt, metadata
