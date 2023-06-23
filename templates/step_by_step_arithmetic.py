from .utils import Template, sample_from, sample_small_int
import random
import tiktoken
from typing import Tuple, List
import math
from functools import reduce


class StepByStepArithmetic(Template):

    def generate(self, n_add=10, n_sub=10) -> List[Tuple[str, dict]]:

        def samp():
            return sample_small_int(dist_args={'x_min': 10})

        additions = [self.add_large_numbers(samp(), samp()) for _ in range(n_add)]
        subtractions = [self.subtract_large_numbers(samp(), samp()) for _ in range(n_sub)]
        return additions + subtractions
    
    def get_metadata(self, txt, kind):

        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(txt)

        metadata = {
            'char_len': len(txt),
            'tokens': tokens,
            'tokenizer': "cl100k_base",
            'tokens_len': len(tokens),
            'data_type': 'step_by_step_arithmetic',
            'kind': kind
        }

        return metadata

    def add_large_numbers(self, num1, num2):
        # convert numbers to strings for easy manipulation
        str_num1 = str(num1)
        str_num2 = str(num2)

        # Make the numbers of same length
        len_diff = len(str_num1) - len(str_num2)
        if len_diff > 0:
            str_num2 = '0' * len_diff + str_num2
        elif len_diff < 0:
            str_num1 = '0' * (-len_diff) + str_num1

        # Add zeros at the beginning of result and carry for alignment purposes
        result = '0' * (len(str_num1) + 1)
        carry = '0' * (len(str_num1) + 1)

        txt = str(num1) + " + " + str(num2) + "\n\n"

        for i in range(len(str_num1)-1, -1, -1):
            temp_result = int(str_num1[i]) + int(str_num2[i])
            if carry[i+1] != '0':
                temp_result += int(carry[i+1])
            carry = carry[:i] + str(temp_result // 10) + carry[i+1:]
            result = result[:i+1] + str(temp_result % 10) + result[i+2:]

            txt += "\n " + str(carry)
            txt += "\n  " + str_num1
            txt += "\n  " + str_num2
            txt += "\n+ " + '-' * len(str_num1)
            txt += "\n " + str(result)
            txt += "\n\n"

        return txt, self.get_metadata(txt, "addition")
    
    def subtract_large_numbers(self, num1, num2):

        num1, num2 = max(num1, num2), min(num1, num2)

        # convert numbers to strings for easy manipulation
        str_num1 = str(num1)
        str_num2 = str(num2)

        # Make the numbers of same length
        len_diff = len(str_num1) - len(str_num2)
        if len_diff > 0:
            str_num2 = '0' * len_diff + str_num2
        elif len_diff < 0:
            str_num1 = '0' * (-len_diff) + str_num1

        # Add zeros at the beginning of result for alignment purposes
        result = '0' * (len(str_num1))

        txt = str(num1) + " - " + str(num2) + "\n\n"

        borrow = 0
        for i in range(len(str_num1)-1, -1, -1):
            temp_result = int(str_num1[i]) - int(str_num2[i]) - borrow
            if temp_result < 0:
                temp_result += 10
                borrow = 1
            else:
                borrow = 0
            result = result[:i] + str(temp_result) + result[i+1:]

            txt += "\nBorrow: " + str(borrow)
            txt += "\n  " + str_num1
            txt += "\n  " + str_num2
            txt += "\n- " + '-' * len(str_num1)
            txt += "\n  " + str(result)
            txt += "\n\n"

            txt += str(result) + "\n"

        return txt, self.get_metadata(txt, 'subtraction')


    
        


